#!/usr/bin/env python3

import argparse
import json
import os
import sys
from pathlib import Path


def normalize(value: str) -> str:
    return value.strip().lower()


def matches(item, technology_stack, purpose, scenario, commit_required):
    if normalize(item["technologyStack"]) != normalize(technology_stack):
        return False

    if normalize(item["purpose"]) != normalize(purpose):
        return False

    item_scenario = normalize(item.get("scenario", ""))
    requested_scenario = normalize(scenario)

    # Empty scenario means "no scenario-specific filtering".
    if requested_scenario and item_scenario != requested_scenario:
        return False

    return bool(item.get("commitRequired", False)) == commit_required


def discover(catalog, technology_stack, purpose, scenario, commit_required):
    matches_found = [
        item
        for item in catalog
        if matches(
            item,
            technology_stack,
            purpose,
            scenario,
            commit_required,
        )
    ]

    if not matches_found:
        raise ValueError(
            "No test-data template matched the supplied "
            "technology stack, purpose, scenario and commit requirement."
        )

    if len(matches_found) > 1:
        raise ValueError(
            f"Multiple test-data templates matched ({len(matches_found)}). "
            "Make the catalog entries more specific."
        )

    return matches_found[0]


def write_github_output(values):
    output_file = os.getenv("GITHUB_OUTPUT")
    if not output_file:
        return

    with open(output_file, "a", encoding="utf-8") as file:
        for key, value in values.items():
            file.write(f"{key}={value}\n")


def main():
    parser = argparse.ArgumentParser(description="Discover CI/CD test-data template.")
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--technology-stack", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--scenario", default="")
    parser.add_argument("--commit-required", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    commit_required = normalize(args.commit_required) == "true"

    catalog_path = Path(args.catalog)
    with catalog_path.open("r", encoding="utf-8") as file:
        catalog = json.load(file)

    result = discover(
        catalog=catalog,
        technology_stack=args.technology_stack,
        purpose=args.purpose,
        scenario=args.scenario,
        commit_required=commit_required,
    )

    output = {
        "repository": result["repository"],
        "base_branch": result["baseBranch"],
        "commit_required": result.get("commitRequired", False),
        "technology_stack": result["technologyStack"],
        "purpose": result["purpose"],
        "scenario": result.get("scenario", ""),
    }

    Path(args.output).write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    write_github_output(
        {
            "repository": output["repository"],
            "base_branch": output["base_branch"],
            "commit_required": str(output["commit_required"]).lower(),
        }
    )

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
