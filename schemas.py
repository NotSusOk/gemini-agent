"""JSON Schemas for hermes-shadow-clone tools."""

SPAWN_SHADOW_CLONES_SCHEMA = {
    "name": "spawn_shadow_clones",
    "description": (
        "Spawn a parallel swarm of independent Gemini 'Shadow Clones' with distinct "
        "specialist personas (Pragmatic Architect, Adversarial Red-Teamer, Performance Optimizer, "
        "or custom roles) to solve a hard coding, architecture, or debugging problem concurrently. "
        "Includes automatic multi-model quota failover, cross-clone judging, a 0-100 arena scoreboard, "
        "and a synthesized best-of-all solution."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "problem": {
                "type": "string",
                "description": "The technical question, bug report, code snippet, or architecture decision to analyze.",
            },
            "context": {
                "type": "string",
                "description": "Optional code context, constraints, or file snippets.",
            },
            "personas": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Optional custom list of clone personas. Defaults to: "
                    "['Pragmatic Architect', 'Adversarial Security & Bug Hunter', 'Performance & Scale Engineer']."
                ),
            },
            "notify_telegram": {
                "type": "boolean",
                "description": "Whether to broadcast the Arena Scoreboard and winning synthesis to Telegram (default: true if configured).",
            },
        },
        "required": ["problem"],
    },
}

SHADOW_VERIFY_CLAIM_SCHEMA = {
    "name": "shadow_verify_claim",
    "description": (
        "Run an independent Adversarial Shadow Clone audit on a proposed patch, shell command, "
        "or technical claim to catch hallucinations, missing edge cases, or subtle bugs before execution."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "claim_or_patch": {
                "type": "string",
                "description": "The proposed code diff, command, or claim to verify.",
            },
            "evidence": {
                "type": "string",
                "description": "Supporting test output, file contents, or requirements to check against.",
            },
        },
        "required": ["claim_or_patch"],
    },
}

SHADOW_ARENA_STATS_SCHEMA = {
    "name": "shadow_arena_stats",
    "description": (
        "Retrieve Shadow Clone Arena battle history, persona win rates, model failover metrics, "
        "and average parallel latency."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "limit": {
                "type": "integer",
                "description": "Number of recent arena battles to include (default: 5).",
            }
        },
    },
}
