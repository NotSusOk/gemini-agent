#!/usr/bin/env python3
"""Bot Telegram ↔ Agent Gemini (agent.py + memory.py) — agent có tool + trí nhớ."""
import os, logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from agent import chay_agent

TOKEN_FILE = os.path.expanduser("~/.qwen_bot_token")

async def start(update, context):
    await update.message.reply_text(
        "👋 Chào! Tao là **Gemi** — agent có tool + trí nhớ.\n"
        "Thử: tính toán, đọc file, hoặc bảo tao nhớ gì đó!"
    )

async def chat(update, context):
    await update.message.chat.send_chat_action(action="typing")
    try:
        # Chạy vòng lặp agent (tool + memory) trong thread riêng — tránh block polling
        ket_qua = await asyncio.to_thread(chay_agent, update.message.text)
        await update.message.reply_text(ket_qua.strip())
    except Exception as e:
        logging.error("Lỗi agent: %s", e)
        await update.message.reply_text(f"⚠️ Lỗi: {e}")

app = Application.builder().token(open(TOKEN_FILE).read().strip()).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
print("Bot Gemi (agent) chạy — polling...")
app.run_polling(allowed_updates=Update.ALL_TYPES)
