from __future__ import annotations

import json
from pathlib import Path

import pytest

from runtime_failover.config import load_config
from runtime_failover.simulator import simulate_route


ROOT = Path(__file__).parents[1]
CONFIG = load_config(ROOT / "examples" / "runtime-failover.json")
OUTCOMES = json.loads((ROOT / "examples" / "outcomes-recovery.json").read_text(encoding="utf-8"))


def test_simulator_selects_third_candidate_after_retryable_failures() -> None:
    result = simulate_route(CONFIG, "quality", OUTCOMES)

    assert result["status"] == "SELECTED"
    assert result["selected"] == "provider-c/fast"
    assert [attempt["outcome"] for attempt in result["attempts"]] == ["timeout", "rate_limited", "success"]


def test_simulator_fails_closed_on_non_retryable_outcome() -> None:
    result = simulate_route(CONFIG, "quality", {"provider-a/quality": "auth_error"})

    assert result["status"] == "BLOCKED"
    assert result["selected"] is None
    assert result["reason"] == "non-retryable outcome: auth_error"
    assert len(result["attempts"]) == 1


def test_simulator_reports_exhaustion() -> None:
    outcomes = {
        "provider-a/quality": "timeout",
        "provider-b/balanced": "unavailable",
        "provider-c/fast": "rate_limited",
    }

    result = simulate_route(CONFIG, "quality", outcomes)

    assert result["status"] == "EXHAUSTED"
    assert result["selected"] is None
    assert len(result["attempts"]) == 3


def test_simulator_rejects_unknown_route() -> None:
    with pytest.raises(ValueError, match="unknown route: missing"):
        simulate_route(CONFIG, "missing", {})
