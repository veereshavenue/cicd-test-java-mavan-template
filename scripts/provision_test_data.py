#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys


def run(command):
    print("$", " ".join(command))
    subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Create a test branch from a discovered template repository."
    )
    parser.add_argument("--template-repository", required=True)
    parser.add_argument("--base-branch", required=True)
    parser.add_argument("--test-repository", required=True)
    parser.add_argument("--test-branch", required=True)
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN")
    if not token:
        raise RuntimeError("GH_TOKEN is required.")

    # This implementation creates a branch in an existing test repository.
    # Repository creation can be added later if the platform standard permits it.
    run([
        "gh", "api",
        f"repos/{args.test_repository}/git/ref",
        "-f", f"ref=refs/heads/{args.test_branch}",
        "-f", f"sha=$(gh api repos/{args.test_repository}/git/ref/heads/{args.base_branch} --jq .object.sha)",
    ])


if __name__ == "__main__":
    try:
        main()
    except (subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
