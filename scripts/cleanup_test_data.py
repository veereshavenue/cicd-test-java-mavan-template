#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description="Delete a temporary test branch.")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--branch", required=True)
    args = parser.parse_args()

    if not os.environ.get("GH_TOKEN"):
        raise RuntimeError("GH_TOKEN is required.")

    subprocess.run(
        [
            "gh",
            "api",
            "--method",
            "DELETE",
            f"repos/{args.repository}/git/refs/heads/{args.branch}",
        ],
        check=True,
    )

    print(f"Deleted branch {args.repository}:{args.branch}")


if __name__ == "__main__":
    try:
        main()
    except (subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
