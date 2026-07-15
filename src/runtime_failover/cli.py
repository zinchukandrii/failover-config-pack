"""Small CLI for validating configuration and demonstrating a deterministic route."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import ConfigValidationError, load_config
from .simulator import simulate_route


def main() -> None:
    parser = argparse.ArgumentParser(prog="runtime-failover")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate a provider-neutral JSON policy")
    validate.add_argument("config", type=Path)

    simulate = subparsers.add_parser("simulate", help="simulate a route without provider calls")
    simulate.add_argument("config", type=Path)
    simulate.add_argument("route")
    simulate.add_argument("outcomes", type=Path, help="JSON object mapping candidate IDs to outcomes")

    args = parser.parse_args()
    try:
        config = load_config(args.config)
        if args.command == "validate":
            print(json.dumps({"status": "VALID", "routes": [route["id"] for route in config["routes"]]}, indent=2))
            return
        outcomes = json.loads(args.outcomes.read_text(encoding="utf-8"))
        if not isinstance(outcomes, dict) or not all(isinstance(key, str) and isinstance(value, str) for key, value in outcomes.items()):
            raise ConfigValidationError("outcomes must be a JSON object of string candidate IDs to string outcomes")
        print(json.dumps(simulate_route(config, args.route, outcomes), indent=2))
    except ConfigValidationError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
