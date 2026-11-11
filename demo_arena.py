#!/usr/bin/env python3
"""Interactive English CLI Demo for hermes-shadow-clone (90s Hackathon Video Runner)."""
from __future__ import annotations

import json
import sys
from tools import handle_shadow_arena_stats, handle_shadow_verify_claim, handle_spawn_shadow_clones


def run_full_showcase(problem: str) -> None:
    print("\n" + "═" * 76)
    print("🥷  HERMES SHADOW-CLONE SWARM — PARALLEL MULTI-MODEL ARENA")
    print("═" * 76)
    print(f"📌 Engineering Problem:\n   {problem}\n")
    print("⚡ [Stage 1/3] Dispatching 3 Concurrent Gemini Shadow Clones:")
    print("   ├─ 🏗️  Clone #1: Pragmatic Architect        (Clean & minimal design)")
    print("   ├─ 🛡️  Clone #2: Adversarial Red-Teamer     (Race conditions & security)")
    print("   └─ ⚡  Clone #3: Performance Optimizer      (Low-latency & throughput)\n")

    raw_arena = handle_spawn_shadow_clones({"problem": problem})
    arena_data = json.loads(raw_arena)
    print(arena_data["arena_report"])

    print("\n" + "─" * 76)
    print("⚖️  [Stage 2/3] Adversarial Claim & Patch Auditor (shadow_verify_claim)")
    print("─" * 76)
    sample_patch = (
        "Claim: 'Fixed duplicate Stripe webhook processing by checking `if not db.exists(event_id)` "
        "before charging the customer (without a database transaction or unique constraint).'"
    )
    print(f"🔍 Auditing Patch:\n   {sample_patch}\n")
    raw_verify = handle_shadow_verify_claim(
        {
            "claim_or_patch": sample_patch,
            "evidence": "High-concurrency async workers handling 500 webhooks/sec.",
        }
    )
    verify_data = json.loads(raw_verify)
    print(f"🛡️  Auditor Model: {verify_data['auditor_model']} ({verify_data['latency_ms']} ms)")
    print(f"📋 Audit Verdict:\n{verify_data['audit_result']}")

    print("\n" + "─" * 76)
    print("📈 [Stage 3/3] Arena Telemetry & Quota Failover Stats (shadow_arena_stats)")
    print("─" * 76)
    stats = json.loads(handle_shadow_arena_stats({"limit": 2}))
    print(
        json.dumps(
            {
                "total_battles": stats["total_battles"],
                "win_counts": stats["win_counts"],
                "total_quota_failovers_survived": stats["total_quota_failovers_survived"],
            },
            indent=2,
        )
    )
    print("═" * 76 + "\n")


if __name__ == "__main__":
    default_problem = (
        "Our Python async webhook worker occasionally processes the same Stripe payment event "
        "twice under high concurrency when Redis briefly times out. How should we fix it?"
    )
    user_problem = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else default_problem
    run_full_showcase(user_problem)
