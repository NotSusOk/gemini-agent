# Gemi — Telegram AI Agent

A Telegram AI agent built with Python that can:
- 💬 Chat naturally in Vietnamese/English (Gemini API)
- 🧠 Remember users across sessions (JSON memory)
- 🛠️ Use tools: calculator, file reader, terminal commands
- 📅 Manage class schedules with natural language (add/change/cancel lessons)
- 🔄 Auto-failover between Gemini models when quota is used up

## Setup

```bash
pip install openai python-telegram-bot
cp config.example.py config.py   # then edit config.py with your keys
```

## Run

```bash
python3 telegram_bot.py
```

## Files

- `agent.py` — agent loop: model ↔ tools ↔ memory
- `memory.py` — persistent memory (JSON)
- `lich_hoc.py` — class schedule manager with exceptions
- `config.example.py` — config template (copy to config.py)
- `telegram_bot.py` — Telegram interface

## ⚠️ Security

Never commit `config.py` — it contains your real API keys. Only commit `config.example.py`.
