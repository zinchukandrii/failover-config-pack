from __future__ import annotations

import json
from pathlib import Path

import pytest

from runtime_failover.config import ConfigValidationError, load_config, validate_config


EXAMPLE = Path(__file__).parents[1] / "examples" / "runtime-failover.json"


def test_example_configuration_is_valid() -> None:
    config = load_config(EXAMPLE)

    assert config["version"] == "1.0"
    assert [route["id"] for route in config["routes"]] == ["quality", "batch"]


def test_validator_reports_duplicate_route_and_candidate_ids() -> None:
    payload = {
        "version": "1.0",
        "policy": {"request_timeout_seconds": 10, "retryable_outcomes": ["timeout"]},
        "routes": [
            {"id": "quality", "candidates": [{"id": "one", "tier": 1}, {"id": "one", "tier": 2}]},
            {"id": "quality", "candidates": [{"id": "two", "tier": 1}]},
        ],
    }

    errors = validate_config(payload)

    assert "duplicate route id: quality" in errors
    assert "duplicate candidate id in route quality: one" in errors


def test_validator_rejects_boolean_numeric_values() -> None:
    payload = {
        "version": "1.0",
        "policy": {"request_timeout_seconds": True, "retryable_outcomes": ["timeout"]},
        "routes": [{"id": "quality", "candidates": [{"id": "one", "tier": True}]}],
    }

    errors = validate_config(payload)

    assert "policy.request_timeout_seconds must be a positive integer" in errors
    assert "routes[0].candidates[0].tier must be a positive integer" in errors


def test_load_config_fails_closed_for_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "broken.json"
    path.write_text("{", encoding="utf-8")

    with pytest.raises(ConfigValidationError, match="Invalid JSON"):
        load_config(path)


def test_load_config_fails_closed_for_schema_defects(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps({"version": "0.9", "routes": []}), encoding="utf-8")

    with pytest.raises(ConfigValidationError, match="version must be '1.0'"):
        load_config(path)
