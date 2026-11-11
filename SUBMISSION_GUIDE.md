# 🏆 Hermes Agent Plugin Hackathon — Ready-to-Use English Submission Kit

## 1. X (Twitter) Post Copy (Tag `@NousResearch` + attach <90s video)

```text
Built `hermes-shadow-clone` for the @NousResearch Hermes Agent Plugin Hackathon! 🥷⚡

Instead of relying on a single thread of reasoning for tough bugs, Hermes can now spawn a parallel swarm of specialist Gemini Shadow Clones (🏗️ Architect, 🛡️ Red-Teamer, ⚡ Optimizer) with automatic multi-model quota failover, cross-clone Arena Judging (0-100), and live Telegram battle reports!

🔗 Plugin Repo: https://github.com/NotSusOk/gemini-agent
#HermesAgent #NousResearch #AIAgents
```

---

## 2. Pull Request to `NousResearch/hermes-agent`

### File to add: `plugin-catalog/hermes-shadow-clone.yaml`
```yaml
name: hermes-shadow-clone
description: "Parallel Gemini shadow-clone swarm & second-opinion arena with automatic quota failover, adversarial claim verification, and optional Telegram live battle reports (calls Google Gemini API via GEMINI_API_KEY and optional Telegram Bot API)."
repo: https://github.com/NotSusOk/gemini-agent
sha: <YOUR_40_CHAR_COMMIT_SHA>
tier: community
```

### Pull Request Title
```text
plugin-catalog: add hermes-shadow-clone (Plugin Hackathon entry)
```

### Pull Request Description
```markdown
## Summary
Adds **`hermes-shadow-clone`** to the Hermes Agent Plugin Catalog for the Hermes Agent Plugin Hackathon.

### What it does
- **`spawn_shadow_clones` (Tool)**: Spawns concurrent Gemini "Shadow Clones" (`Pragmatic Architect`, `Adversarial Red-Teamer`, `Performance Optimizer`, or custom personas) in parallel via `ThreadPoolExecutor`, rotates across a multi-model Gemini cascade (`gemini-3.6-flash` -> `gemini-3.5-flash` -> `gemini-3-flash-preview` -> `gemini-3.5-flash-lite` -> `gemini-2.5-flash`) with automatic `HTTP 429` quota failover, runs an **Arena Judge** (`0-100` scoreboard + blind-spot detection), and returns a synthesized best-of-all solution.
- **`shadow_verify_claim` (Tool)**: Runs an independent adversarial audit on a proposed patch, shell command, or technical claim (`PASS` / `WARN` / `BLOCK` + risk score).
- **`shadow_arena_stats` (Tool)**: Queries durable Arena telemetry (persona win rates, quota failovers survived, parallel latency).
- **`post_tool_call` (Hook)**: Monitors consecutive tool execution errors.
- **Optional Telegram Arena Integration**: Broadcasts live Arena scoreboards to Telegram when `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set.

### Validation & Security Disclosures
- Zero third-party Python dependencies required for the core plugin (uses Python stdlib `urllib.request` & `concurrent.futures`).
- External network calls: Google Gemini OpenAI-compatible API (`GEMINI_API_KEY`) and optional Telegram Bot API (`TELEGRAM_BOT_TOKEN`).
- Validated with `test_validate.py` and `hermes plugins validate`.
```

---

## 3. 90-Second Video Recording Script (English — Split Screen: Terminal + Telegram)

- **0:00 – 0:15 (Show `plugin.yaml` & `README.md`)**:
  Show the plugin directory (`plugin.yaml`, `__init__.py`, `schemas.py`, `tools.py`) and run:
  ```bash
  python3 test_validate.py
  ```
- **0:15 – 0:50 (Run the 3-Stage CLI Arena Showcase)**:
  Run in terminal:
  ```bash
  python3 demo_arena.py
  ```
  Highlight on screen:
  1. **3 Clones racing in parallel** (🏗️ Pragmatic Architect vs. 🛡️ Adversarial Red-Teamer vs. ⚡ Performance Optimizer).
  2. **The Scoreboard (`0-100`) & Winner (`👑`)**, plus the **Blind Spots Caught** and **Synthesized Best Solution**.
  3. **Stage 2 (`shadow_verify_claim`)** catching a race-condition bug in a naive webhook patch.
- **0:50 – 1:20 (Show Live Telegram Bot Arena)**:
  Run `python3 telegram_arena_bot.py`, open your Telegram bot, and tap `/start` -> `/demo` -> `/stats` to show the English Shadow Clone Scoreboard appearing live in Telegram!
