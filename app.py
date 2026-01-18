import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

load_dotenv()

app = Flask(__name__)

# --- Tool with Validation & Default Logic ---

@tool
def get_daily_prayer_times(city: str = "lahore"):
    """
    Get daily prayer times for a city in Pakistan. 
    Also please provide specific prayer time if asked
    Defaults to 'lahore' if no city is provided.
    """
    clean_city = city.lower().strip()
    url = f"http://api.aladhan.com/v1/timingsByCity?city={clean_city}&country=Pakistan&method=1"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        # Validation: Check if API returned success
        if response.status_code != 200 or data.get('code') != 200:
            return f"Error: '{clean_city}' is not a valid city in Pakistan. Please check spelling."

        t = data['data']['timings']
        return f"Times for {clean_city}: Fajr:{t['Fajr']}, Dhuhr:{t['Dhuhr']}, Asr:{t['Asr']}, Maghrib:{t['Maghrib']}, Isha:{t['Isha']}"

    except Exception:
        return "Service temporarily unavailable. Please try again later."

# Initialize Model
model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
tool_model = model.bind_tools([get_daily_prayer_times])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "").lower().strip()
    
    # Start the message history with a System Message for better results
    messages = [
        SystemMessage(content=(
            "You are a helpful Pakistani prayer time assistant. "
            "1. Use the tool to fetch prayer data. "
            "2. If the user asks for a SPECIFIC prayer (e.g., 'What time is Fajr?'), "
            "extract ONLY that timing from the tool's result and answer concisely. "
            "3. If no city is mentioned, use Lahore as the default. "
            "4. Always be polite and respectful."

        )),
        HumanMessage(content=user_input)
    ]
    
    
    # Step 1: First model call to see if it wants to use a tool
    ai_msg = tool_model.invoke(messages)
    messages.append(ai_msg)

    # Step 2: If the model generated tool_calls, execute them
    if ai_msg.tool_calls:
        for tool_call in ai_msg.tool_calls:
            # Execute the actual tool function
            result = get_daily_prayer_times.invoke(tool_call)
            # IMPORTANT: Wrap result in a ToolMessage so the LLM knows it's the answer
            messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
        
        # Step 3: THE FIX - Call the model AGAIN with the tool result in history
        # This generates the final human answer like "The Maghrib time in Lahore is 6:00 PM."
        final_response = tool_model.invoke(messages)
        return jsonify({"response": final_response.content})
    
    # If no tool was needed, just return the direct content
    return jsonify({"response": ai_msg.content})

if __name__ == '__main__':
    app.run(debug=True)