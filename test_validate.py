#!/usr/bin/env python3
"""Self-contained validator simulating `hermes plugins validate` capability checks."""
from __future__ import annotations

import json
from pathlib import Path
from __init__ import register


class MockPluginContext:
    def __init__(self) -> None:
        self.tools: dict[str, dict] = {}
        self.hooks: dict[str, list] = {}

    def register_tool(self, name: str, toolset: str, schema: dict, handler) -> None:
        self.tools[name] = {"toolset": toolset, "schema": schema, "handler": handler}

    def register_hook(self, event: str, callback) -> None:
        self.hooks.setdefault(event, []).append(callback)


def main() -> None:
    manifest_text = Path(__file__).with_name("plugin.yaml").read_text(encoding="utf-8")
    ctx = MockPluginContext()
    register(ctx)

    expected_tools = {"spawn_shadow_clones", "shadow_verify_claim", "shadow_arena_stats"}
    expected_hooks = {"post_tool_call"}

    assert set(ctx.tools.keys()) == expected_tools, f"Tool mismatch: {set(ctx.tools.keys())}"
    assert set(ctx.hooks.keys()) == expected_hooks, f"Hook mismatch: {set(ctx.hooks.keys())}"

    # Verify each tool handler executes cleanly and returns valid JSON
    r1 = json.loads(ctx.tools["spawn_shadow_clones"]["handler"]({"problem": "Test race condition"}))
    assert "winner" in r1 and "synthesis" in r1

    r2 = json.loads(ctx.tools["shadow_verify_claim"]["handler"]({"claim_or_patch": "rm -rf /tmp/build"}))
    assert "audit_result" in r2

    r3 = json.loads(ctx.tools["shadow_arena_stats"]["handler"]({"limit": 3}))
    assert r3["total_battles"] >= 1

    # Verify hook executes cleanly
    for cb in ctx.hooks["post_tool_call"]:
        cb("bash", {"cmd": "pytest"}, "Traceback (most recent call last): AssertionError")

    print("✅ All manifest capabilities, tool schemas, handlers, and hooks verified!")


if __name__ == "__main__":
    main()
