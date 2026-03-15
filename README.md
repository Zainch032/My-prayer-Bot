---
title: My Prayer Bot
emoji: 🕌
colorFrom: green
colorTo: blue
sdk: docker
app_file: main.py
pinned: false
---

# 🕌 Pakistan Prayer Assistant (Agentic AI)

A specialized AI-powered prayer timing assistant designed for accuracy across all major cities in Pakistan. Unlike general LLMs which often provide outdated or estimated timings, this assistant uses **Tool-Calling (Agentic AI)** to retrieve real-time data directly from the Aladhan API.

---

## 🚀 Why This Project?
General AI models (like ChatGPT) suffer from "knowledge cutoff" and often fail to provide exact, real-time prayer timings because:
* **Dynamic Calculations:** Prayer times change daily based on the sun's position.
* **Localization:** General models may confuse methods (Hanafi vs Shafi'i) or specific city coordinates.
* **Reliability:** This project uses an **AI Agent loop**. Instead of guessing, the AI thinks: *"I need the exact time for Lahore,"* calls a verified tool, and then provides the answer.

---

## 🛠️ Features
* **Real-time Data:** Fetches live timings from the Aladhan API.
* **Specific Queries:** Ask for just one time (e.g., "When is Maghrib?") or the full schedule.
* **Natural Language:** Understands conversational Urdu/English inputs.
* **Tactile UI:** A modern, medium-sized chat interface with 3D button effects and smooth animations.

## 🌐 Live Demo

You can try the live version of this app here: [My Prayer Bot on Hugging Face Spaces](https://huggingface.co/spaces/Zainch032/My-prayer-Bot)

---

## 🧠 How It Works (Tool Calling / Agentic Loop)

This project uses **tool calling** with LangChain and Groq to fetch live prayer times instead of guessing:

1. **User Query:** The user types something like *"What time is Maghrib in Lahore?"* into the chat UI.
2. **System + Human Messages:** The backend builds a message list that includes a system prompt (explaining that the model should use tools for prayer times) and the user’s message.
3. **First Model Call (Decide to Use Tool):** The LangChain `ChatGroq` model is called with these messages and is bound to the Python tool `get_daily_prayer_times`. The model decides whether it needs to call the tool and, if yes, creates a **tool call** with the city it inferred from the user’s text.
4. **Tool Execution:** The Python function `get_daily_prayer_times` runs, calls the **Aladhan API**, validates the response, and returns a clean text summary of all prayer times for that city.
5. **Tool Result Message:** The backend wraps this result inside a `ToolMessage` and appends it to the conversation history so the model can “see” the tool’s output.
6. **Second Model Call (Final Answer):** The model is called again with the updated history (including the tool result). It then picks out the exact timing requested (e.g., just Maghrib) and generates a short, user-friendly answer.
7. **Response to User:** The final text is sent back as JSON, and the frontend displays it in the chat bubble.

---


## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

