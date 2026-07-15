"""Deterministic, side-effect-free failover simulation."""

from __future__ import annotations

from typing import Any


def simulate_route(config: dict[str, Any], route_id: str, outcomes: dict[str, str]) -> dict[str, Any]:
    """Simulate one ordered route from declared outcomes only.

    No provider calls are made. A candidate succeeds only when its supplied outcome is
    ``success``; retryable failures advance to the next declared candidate. Any unknown
    outcome fails closed so the caller cannot silently treat it as a successful response.
    """
    route = next((item for item in config["routes"] if item["id"] == route_id), None)
    if route is None:
        raise ValueError(f"unknown route: {route_id}")

    retryable = set(config["policy"]["retryable_outcomes"])
    attempts: list[dict[str, str | int]] = []
    for position, candidate in enumerate(route["candidates"], start=1):
        candidate_id = candidate["id"]
        outcome = outcomes.get(candidate_id, "unavailable")
        attempt = {"position": position, "candidate_id": candidate_id, "tier": candidate["tier"], "outcome": outcome}
        attempts.append(attempt)
        if outcome == "success":
            return {"route_id": route_id, "status": "SELECTED", "selected": candidate_id, "attempts": attempts}
        if outcome not in retryable:
            return {"route_id": route_id, "status": "BLOCKED", "selected": None, "attempts": attempts, "reason": f"non-retryable outcome: {outcome}"}

    return {"route_id": route_id, "status": "EXHAUSTED", "selected": None, "attempts": attempts, "reason": "all candidates returned retryable failures"}
