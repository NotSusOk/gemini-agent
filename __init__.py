"""hermes-shadow-clone: Parallel Gemini Swarm & Second-Opinion Arena for Hermes Agent."""
from __future__ import annotations

try:
    from .schemas import (
        SHADOW_ARENA_STATS_SCHEMA,
        SHADOW_VERIFY_CLAIM_SCHEMA,
        SPAWN_SHADOW_CLONES_SCHEMA,
    )
    from .tools import (
        handle_shadow_arena_stats,
        handle_shadow_verify_claim,
        handle_spawn_shadow_clones,
    )
except ImportError:
    from schemas import (
        SHADOW_ARENA_STATS_SCHEMA,
        SHADOW_VERIFY_CLAIM_SCHEMA,
        SPAWN_SHADOW_CLONES_SCHEMA,
    )
    from tools import (
        handle_shadow_arena_stats,
        handle_shadow_verify_claim,
        handle_spawn_shadow_clones,
    )

_consecutive_tool_errors = 0


def register(ctx) -> None:
    """Register Shadow Clone tools and lifecycle hooks with Hermes Agent."""
    ctx.register_tool(
        name="spawn_shadow_clones",
        toolset="shadow_clone",
        schema=SPAWN_SHADOW_CLONES_SCHEMA,
        handler=handle_spawn_shadow_clones,
    )
    ctx.register_tool(
        name="shadow_verify_claim",
        toolset="shadow_clone",
        schema=SHADOW_VERIFY_CLAIM_SCHEMA,
        handler=handle_shadow_verify_claim,
    )
    ctx.register_tool(
        name="shadow_arena_stats",
        toolset="shadow_clone",
        schema=SHADOW_ARENA_STATS_SCHEMA,
        handler=handle_shadow_arena_stats,
    )

    def on_post_tool_call(tool_name: str, params=None, result=None, **kwargs):
        global _consecutive_tool_errors
        text = str(result or "")
        is_err = any(
            marker in text.lower()
            for marker in ("traceback (most recent call last)", "error:", "exception:", "command exited with code")
        )
        if is_err and tool_name not in ("spawn_shadow_clones", "shadow_verify_claim"):
            _consecutive_tool_errors += 1
        else:
            _consecutive_tool_errors = 0

    ctx.register_hook("post_tool_call", on_post_tool_call)
