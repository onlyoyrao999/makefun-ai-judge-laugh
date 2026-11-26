#!/usr/bin/env python3
"""Entry for make.fun's "Make the AI Judge Laugh" bounty.

The program produces a single office joke and saves it where the
grader looks for it. The joke leans on a shared office frustration:
a printer never misbehaves on a quiet afternoon, only when a
deadline is minutes away — so the punchline treats the printer as
the office's most dependable employee, the one that never misses
a deadline (because it makes sure you do).
"""

import argparse
import os
import sys

JOKE = (
    "The office printer only jams when the deadline is five minutes away: "
    "it is the only colleague that never misses one."
)

FALLBACK_PATH = "/output/entry.txt"
MAX_CHARS = 200


def problems_with(line):
    """Check a candidate line against the bounty gate.

    Returns a list of issues; an empty list means the line passes:
    non-blank, at most 200 UTF-8 characters, exactly one line.
    """
    issues = []
    if not line.strip():
        issues.append("entry is blank")
    size = len(line.encode("utf-8"))
    if size > MAX_CHARS:
        issues.append(f"entry is {size} bytes, over the 200 limit")
    if len(line.strip().splitlines()) > 1:
        issues.append("entry must be exactly one line")
    return issues


def save_joke(path):
    """Write the joke to path, ending with a newline."""
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(JOKE + "\n")


def load_joke(path):
    """Read back whatever was written to path."""
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def run():
    parser = argparse.ArgumentParser(
        description="Save the office-printer joke to entry.txt.")
    parser.add_argument(
        "--output", default=None,
        help="destination file (default: $ENTRY_OUTPUT or /output/entry.txt)")
    parser.add_argument(
        "--show", action="store_true",
        help="print the joke to stdout as well as saving it")
    options = parser.parse_args()

    issues = problems_with(JOKE)
    if issues:
        for issue in issues:
            print(f"gate failed: {issue}", file=sys.stderr)
        return 1

    if options.show:
        print(JOKE)

    target = options.output or os.environ.get("ENTRY_OUTPUT") or FALLBACK_PATH
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)
    save_joke(target)

    back = load_joke(target)
    if back != JOKE + "\n":
        print("verification failed: file contents differ from the joke",
              file=sys.stderr)
        return 1
    if problems_with(back.strip()):
        print("verification failed: saved file fails the gate",
              file=sys.stderr)
        return 1

    print(f"saved {len(JOKE)}-character joke "
          f"({len(JOKE.split())} words) to {target}, verified")
    return 0


if __name__ == "__main__":
    sys.exit(run())
