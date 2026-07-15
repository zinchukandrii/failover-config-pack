"""Strict, provider-neutral configuration loading and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigValidationError(ValueError):
    """Raised when a runtime failover configuration is unsafe or incomplete."""


def load_config(path: Path) -> dict[str, Any]:
    """Load JSON then fail closed when the document violates the public schema."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ConfigValidationError(f"Could not read configuration: {error}") from error
    except json.JSONDecodeError as error:
        raise ConfigValidationError(f"Invalid JSON: {error.msg}") from error

    errors = validate_config(payload)
    if errors:
        raise ConfigValidationError("; ".join(errors))
    return payload


def validate_config(payload: Any) -> list[str]:
    """Return all deterministic schema defects without resolving any providers."""
    if not isinstance(payload, dict):
        return ["root must be an object"]

    errors: list[str] = []
    if payload.get("version") != "1.0":
        errors.append("version must be '1.0'")

    policy = payload.get("policy")
    if not isinstance(policy, dict):
        errors.append("policy must be an object")
    else:
        timeout = policy.get("request_timeout_seconds")
        if type(timeout) is not int or timeout <= 0:
            errors.append("policy.request_timeout_seconds must be a positive integer")
        retryable = policy.get("retryable_outcomes")
        if not isinstance(retryable, list) or not retryable or not all(
            isinstance(item, str) and item for item in retryable
        ):
            errors.append("policy.retryable_outcomes must be a non-empty list of strings")

    routes = payload.get("routes")
    if not isinstance(routes, list) or not routes:
        return [*errors, "routes must be a non-empty list"]

    route_ids: set[str] = set()
    for index, route in enumerate(routes):
        prefix = f"routes[{index}]"
        if not isinstance(route, dict):
            errors.append(f"{prefix} must be an object")
            continue
        route_id = route.get("id")
        if not isinstance(route_id, str) or not route_id:
            errors.append(f"{prefix}.id must be a non-empty string")
        elif route_id in route_ids:
            errors.append(f"duplicate route id: {route_id}")
        else:
            route_ids.add(route_id)

        candidates = route.get("candidates")
        if not isinstance(candidates, list) or not candidates:
            errors.append(f"{prefix}.candidates must be a non-empty list")
            continue
        candidate_ids: set[str] = set()
        for candidate_index, candidate in enumerate(candidates):
            candidate_prefix = f"{prefix}.candidates[{candidate_index}]"
            if not isinstance(candidate, dict):
                errors.append(f"{candidate_prefix} must be an object")
                continue
            candidate_id = candidate.get("id")
            if not isinstance(candidate_id, str) or not candidate_id:
                errors.append(f"{candidate_prefix}.id must be a non-empty string")
            elif candidate_id in candidate_ids:
                errors.append(f"duplicate candidate id in route {route_id}: {candidate_id}")
            else:
                candidate_ids.add(candidate_id)
            tier = candidate.get("tier")
            if type(tier) is not int or tier < 1:
                errors.append(f"{candidate_prefix}.tier must be a positive integer")
    return errors
