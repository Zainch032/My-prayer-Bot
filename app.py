import os
import requests
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "pakistan-prayer-bot-secret-key-2026")

MAX_MEMORY_TURNS = 6  # Keep last 6 dialogue exchanges in session

# --- Tool with Validation & Default Logic ---

@tool
def get_daily_prayer_times(city: str = "lahore"):
    """
    Get daily prayer times for a city in Pakistan. 
    Also please provide specific prayer time if asked
    Defaults to 'lahore' if no city is provided.
    """
    clean_city = city.lower().strip()
    url = f"https://api.aladhan.com/v1/timingsByCity?city={clean_city}&country=Pakistan&method=1"
    headers = {"User-Agent": "PakistanPrayerBot/1.0"}
    
    try:
        response = requests.get(url, headers=headers, timeout=8)
        data = response.json()

        # Validation: Check if API returned success
        if response.status_code != 200 or data.get('code') != 200:
            return f"Error: '{clean_city}' is not a valid city in Pakistan. Please check spelling."

        t = data['data']['timings']
        return f"Times for {clean_city}: Fajr:{t['Fajr']}, Dhuhr:{t['Dhuhr']}, Asr:{t['Asr']}, Maghrib:{t['Maghrib']}, Isha:{t['Isha']}"

    except Exception:
        return "Service temporarily unavailable. Please try again later."

# Groq retired llama-3.3-70b-versatile (Aug 2026). Override with GROQ_MODEL if needed.
model = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
    temperature=0,
)
tool_model = model.bind_tools([get_daily_prayer_times])

@app.route('/')
def home():
    return render_template('index.html')
@app.get("/health")
def health():
    return {"status": "online", "model_loaded": model is not None}
@app.route('/chat', methods=['POST'])
def chat():
    payload = request.get_json(silent=True) or {}
    user_input = str(payload.get("message", "")).strip()
    if not user_input:
        return jsonify({"response": "Please ask a question about prayer times."}), 400

    # Retrieve short-term conversation memory from session or payload
    raw_history = session.get("chat_history") or payload.get("history") or []
    if not isinstance(raw_history, list):
        raw_history = []

    messages = [
        SystemMessage(content=(
            "You are a helpful Pakistani prayer time assistant. "
            "1. Use the tool to fetch prayer data when needed. "
            "2. If the user asks for a SPECIFIC prayer (e.g., 'What time is Fajr?'), "
            "extract ONLY that timing from the tool's result and answer concisely. "
            "3. If no city is mentioned in the prompt or recent conversation, use Lahore as the default. "
            "4. Maintain context from recent questions (e.g., follow-ups about 'what about Asr?' or another prayer in the same city). "
            "5. Always be polite, concise, and respectful."
        ))
    ]

    # Reconstruct previous turns for memory (last N turns)
    for item in raw_history[-MAX_MEMORY_TURNS * 2:]:
        role = item.get("role")
        content = item.get("content", "")
        if role == "user" and content:
            messages.append(HumanMessage(content=content))
        elif role == "assistant" and content:
            messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=user_input))

    try:
        ai_msg = tool_model.invoke(messages)
        messages.append(ai_msg)

        if ai_msg.tool_calls:
            for tool_call in ai_msg.tool_calls:
                result = get_daily_prayer_times.invoke(tool_call)
                messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))

            final_response = tool_model.invoke(messages)
            answer = final_response.content
        else:
            answer = ai_msg.content

        if isinstance(answer, list):
            answer = "".join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in answer
            )
        answer = (answer or "").strip() or "I could not generate a reply. Please try again."

        # Save conversation memory (trimmed)
        raw_history.append({"role": "user", "content": user_input})
        raw_history.append({"role": "assistant", "content": answer})
        session["chat_history"] = raw_history[-(MAX_MEMORY_TURNS * 2):]

        return jsonify({"response": answer, "history": session["chat_history"]})
    except Exception as exc:
        return jsonify({"response": f"Sorry, I could not fetch prayer times right now. ({exc})"}), 500

@app.route('/reset', methods=['POST'])
def reset_chat():
    session.pop("chat_history", None)
    return jsonify({"status": "cleared"})

if __name__ == '__main__':
    app.run(debug=True)