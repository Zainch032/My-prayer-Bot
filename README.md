---
title: My Prayer Bot
emoji: 🕌
colorFrom: green
colorTo: blue
sdk: docker
app_file: main.py
pinned: false
---

# 🕌 Pakistan Prayer Assistant — Real-Time Agentic AI

> ChatGPT cannot tell you today's exact prayer time. This bot can.

## Live Demo
Try it here: [My Prayer Bot on Hugging Face Spaces](https://huggingface.co/spaces/Zainch032/My-prayer-Bot)

---

## The Problem This Solves

In Pakistan, millions of people need accurate prayer times daily. But:

- ChatGPT and other LLMs **cannot give real-time prayer times** — their training data is outdated
- Prayer times **change every single day** based on the sun's position
- Times differ city by city — Lahore, Karachi, Islamabad, Peshawar all have different timings
- Wrong prayer times = missed prayers

**This bot fixes all of that.**

---

## How Is This Different From ChatGPT?

| | ChatGPT | This Bot |
|---|---|---|
| Prayer times source | Training data (outdated) | Live Aladhan API (real-time) |
| Today's exact time | Cannot know | Always accurate |
| City-specific times | Often wrong | Precise per city |
| Updates daily | Never | Every single day |

---

## Features

- **Real-time data** — fetches live timings from the Aladhan API every time you ask
- **Any Pakistani city** — Lahore, Karachi, Islamabad, Peshawar, Quetta and more
- **Ask naturally** — type in English or Urdu conversationally
- **Single or full schedule** — ask for just Maghrib or the full day's schedule
- **Agentic AI loop** — the model thinks, calls the tool, gets real data, answers accurately

---

## How It Works

1. You ask — *"What time is Maghrib in Lahore today?"*
2. The AI decides it needs real data — it does not guess
3. It calls the **Aladhan API tool** with your city
4. The API returns today's exact prayer times
5. The AI reads the result and gives you a clean precise answer

---

## Tech Stack

- **LangChain + Groq** (llama-3.3-70b) — AI reasoning and tool calling
- **Aladhan API** — real-time prayer times
- **Flask** — backend
- **Docker** — deployment
- **Hugging Face Spaces** — free hosting

---

## Author

**Muhammad Zain** — Final year Data Science student, Lahore, Pakistan

- GitHub: [Zainch032](https://github.com/Zainch032)
- LinkedIn: [Muhammad Zain](https://linkedin.com/in/muhammad-zain-9710692b4)
- Hugging Face: [Zainch032](https://huggingface.co/Zainch032)

---

## License

MIT License