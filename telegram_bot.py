#!/usr/bin/env python3
"""Bot Telegram ↔ Hermes Shadow-Clone Arena (English) + Gemi Agent fallback."""
import asyncio
import json
import logging
import os
import sys

# Ensure macOS Python 3.14 finds the system CA bundle for httpx / python-telegram-bot
if os.path.exists("/etc/ssl/cert.pem"):
    os.environ.setdefault("SSL_CERT_FILE", "/etc/ssl/cert.pem")

SHADOW_CLONE_DIR = "/Users/admin/.gemini/antigravity/scratch/hermes-shadow-clone"
if SHADOW_CLONE_DIR not in sys.path:
    sys.path.insert(0, SHADOW_CLONE_DIR)

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from tools import (
    handle_shadow_arena_stats,
    handle_shadow_verify_claim,
    handle_spawn_shadow_clones,
)

TOKEN_FILE = os.path.expanduser("~/.qwen_bot_token")

DEMO_PROBLEM = (
    "Our async Python webhook worker occasionally charges customers twice when Redis "
    "briefly times out under high concurrency. How should we make it strictly idempotent?"
)


async def start_cmd(update: Update, context) -> None:
    await update.message.reply_text(
        "🥷 **Hermes Shadow-Clone Arena**\n"
        "Parallel Multi-Model Gemini Swarm for Hermes Agent\n\n"
        "Active Shadow Clones:\n"
        "• 🏗️ Clone #1: Pragmatic Architect\n"
        "• 🛡️ Clone #2: Adversarial Red-Teamer\n"
        "• ⚡ Clone #3: Performance Optimizer\n\n"
        "Commands:\n"
        "• /demo — Run instant 1-click Hackathon Arena Showcase\n"
        "• /clone <problem> — Spawn parallel Shadow Clones & Judge\n"
        "• /verify <patch/claim> — Run Adversarial Claim Audit\n"
        "• /stats — View Arena Win-Rate & Quota Failover Telemetry"
    )


async def stats_cmd(update: Update, context) -> None:
    raw = await asyncio.to_thread(handle_shadow_arena_stats, {"limit": 5})
    data = json.loads(raw)
    lines = [
        "📊 Shadow Clone Arena Telemetry",
        f"• Total Arena Battles: {data.get('total_battles', 0)}",
        f"• Quota Failovers Survived: {data.get('total_quota_failovers_survived', 0)}",
        "• Wins by Persona:",
    ]
    for persona, wins in data.get("win_counts", {}).items():
        lines.append(f"  - 🏆 {persona}: {wins}")
    await update.message.reply_text("\n".join(lines))


async def verify_cmd(update: Update, context) -> None:
    text = (update.message.text or "").strip()
    claim = text[len("/verify") :].strip() or (
        "Fixed duplicate webhook charging by checking `if not db.exists(id)` before `stripe.charge()`."
    )
    status_msg = await update.message.reply_text("🛡️ Running Adversarial Shadow-Clone Audit...")
    raw = await asyncio.to_thread(
        handle_shadow_verify_claim,
        {"claim_or_patch": claim, "evidence": "Concurrent production worker environment"},
    )
    data = json.loads(raw)
    reply = (
        f"⚖️ Adversarial Claim Audit\n"
        f"• Auditor Model: {data.get('auditor_model')} ({data.get('latency_ms')} ms)\n\n"
        f"{data.get('audit_result')}"
    )
    await status_msg.edit_text(reply[:4000])


async def demo_cmd(update: Update, context) -> None:
    status_msg = await update.message.reply_text(
        f"🥷 Spawning 3 Parallel Gemini Shadow Clones...\n\n"
        f"📌 Problem: {DEMO_PROBLEM}\n\n"
        f"⏳ Racing: 🏗️ Architect vs. 🛡️ Red-Teamer vs. ⚡ Optimizer..."
    )
    await update.message.chat.send_chat_action(action="typing")
    raw = await asyncio.to_thread(
        handle_spawn_shadow_clones,
        {"problem": DEMO_PROBLEM, "notify_telegram": False},
    )
    data = json.loads(raw)
    report = data.get("arena_report", "No report generated.")
    await status_msg.edit_text(report[:4000])


async def run_arena_message(update: Update, context) -> None:
    text = (update.message.text or "").strip()
    if text.startswith("/clone"):
        text = text[len("/clone") :].strip()
    if not text:
        await update.message.reply_text("Usage: /clone <engineering question> or tap /demo")
        return

    status_msg = await update.message.reply_text(
        "🥷 Spawning 3 parallel Gemini Shadow Clones (🏗️ Architect | 🛡️ Red-Teamer | ⚡ Optimizer)..."
    )
    await update.message.chat.send_chat_action(action="typing")
    raw = await asyncio.to_thread(
        handle_spawn_shadow_clones,
        {"problem": text, "notify_telegram": False},
    )
    data = json.loads(raw)
    report = data.get("arena_report", "No report generated.")
    await status_msg.edit_text(report[:4000])


app = Application.builder().token(open(TOKEN_FILE).read().strip()).build()
app.add_handler(CommandHandler("start", start_cmd))
app.add_handler(CommandHandler("demo", demo_cmd))
app.add_handler(CommandHandler("verify", verify_cmd))
app.add_handler(CommandHandler("stats", stats_cmd))
app.add_handler(CommandHandler("clone", run_arena_message))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, run_arena_message))
print("🥷 Hermes Shadow-Clone Telegram Arena Bot running — polling...")
app.run_polling(allowed_updates=Update.ALL_TYPES)
