# 🥷 hermes-shadow-clone

**Parallel Gemini Shadow-Clone Swarm & Second-Opinion Arena for [Hermes Agent](https://github.com/NousResearch/hermes-agent)**

When Hermes Agent faces a high-stakes bug, concurrency race condition, or architectural trade-off, a single line of reasoning can miss subtle blind spots. `hermes-shadow-clone` lets Hermes spawn a **parallel swarm of specialist Gemini Shadow Clones** that attack the problem concurrently from competing engineering perspectives, score each other in an **Arena Judge**, and return a synthesized best-of-all solution — in the wall-clock latency of a single request.

---

## ✨ Key Features

1. **⚡ Concurrent Multi-Persona Swarm (`spawn_shadow_clones`)**
   - **🏗️ Clone #1 — Pragmatic Architect**: Clean, minimal, maintainable implementation.
   - **🛡️ Clone #2 — Adversarial Red-Teamer**: Hunts for race conditions, injection vectors, and edge-case traps.
   - **⚡ Clone #3 — Performance Optimizer**: Optimizes time/space complexity, batching, and I/O throughput.
   - Supports custom persona lists per invocation.
2. **🔄 Quota-Resilient Multi-Model Failover Cascade**
   - Distributes clones across `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3-flash-preview`, `gemini-3.5-flash-lite`, `gemini-2.5-flash`, and `gemini-2.0-flash`.
   - Automatically fails over on `HTTP 429 (RESOURCE_EXHAUSTED)` or transient model errors so long agent sessions never stall.
3. **⚖️ Adversarial Claim & Patch Auditor (`shadow_verify_claim`)**
   - Cross-examines a proposed code diff, shell command, or technical claim against evidence before execution (`PASS` / `WARN` / `BLOCK` + risk score `0-100`).
4. **📲 Optional Telegram Live Arena Feed (`telegram_arena_bot.py`)**
   - Broadcasts live Arena Scoreboards directly to Telegram (`TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID`) or lets you trigger Shadow Clone battles straight from your phone via `/clone <problem>`.
5. **🪶 Zero Heavy Dependencies**
   - Core plugin uses Python's standard library (`urllib.request`, `concurrent.futures`), passing `hermes plugins validate` cleanly in any environment.

---

## 📦 Installation

### Into Hermes Agent
```bash
mkdir -p ~/.hermes/plugins/hermes-shadow-clone
cp -r . ~/.hermes/plugins/hermes-shadow-clone/
export GEMINI_API_KEY="your-gemini-api-key"

hermes plugins validate ~/.hermes/plugins/hermes-shadow-clone
hermes plugins enable hermes-shadow-clone
```

### Quick CLI Demo
```bash
export GEMINI_API_KEY="your-gemini-api-key"
python3 demo_arena.py "How do we make our webhook consumer idempotent under Redis failover?"
```

### Telegram Arena Bot (Optional)
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
python3 telegram_arena_bot.py
```

---

## 🛠️ Provided Capabilities (`plugin.yaml`)

| Surface | Name | Description |
| :--- | :--- | :--- |
| **Tool** | `spawn_shadow_clones` | Spawns parallel Gemini clones, scores proposals (`0-100`), highlights blind spots caught, and synthesizes the winning solution. |
| **Tool** | `shadow_verify_claim` | Runs an independent adversarial audit on a proposed patch, command, or claim. |
| **Tool** | `shadow_arena_stats` | Returns historical persona win rates, quota failovers survived, and latency stats. |
| **Hook** | `post_tool_call` | Tracks consecutive tool execution errors for diagnostic escalation. |
