#!/usr/bin/env python3
"""Make the AI Judge Laugh: one office-life joke.

Writes one joke about office life to /output/entry.txt (the path the
make.fun program/v1 harness grades).

The joke is built in two halves on purpose: a setup that states a
painfully true office observation — the printer only ever jams when a
deadline is minutes away — then a punchline that turns the printer
into the office's most reliable colleague, the one that never misses
a deadline (by causing you to miss yours).
"""

import argparse
import os
import sys

# The joke, kept as one line of plain text.
SETUP = "The office printer only jams when the deadline is five minutes away:"
PUNCHLINE = "it is the only colleague that never misses one."

JOKE = SETUP + " " + PUNCHLINE

DEFAULT_OUTPUT = "/output/entry.txt"


def build_joke() -> str:
    """Return the single joke line."""
    return JOKE


def parse_args(argv=None):
    """Command-line options for local runs and debugging."""
    parser = argparse.ArgumentParser(
        description="Write the office-life joke to entry.txt.")
    parser.add_argument(
        "--output", default=None,
        help="where to write the joke (default: $ENTRY_OUTPUT or "
             "/output/entry.txt)")
    parser.add_argument(
        "--print", action="store_true",
        help="also print the joke to stdout instead of only writing it")
    return parser.parse_args(argv)


def check_joke(joke: str) -> list:
    """Return a list of gate problems; empty means the joke is valid.

    Mirrors the competition gate: 1-200 UTF-8 characters, not only
    whitespace, a single line of plain text.
    """
    problems = []
    if not joke.strip():
        problems.append("joke is empty or only whitespace")
    if not (1 <= len(joke.encode("utf-8")) <= 200):
        problems.append(
            f"joke is {len(joke.encode('utf-8'))} bytes, outside 1-200")
    if "\n" in joke.strip():
        problems.append("joke must be a single line")
    return problems


def main(argv=None) -> int:
    args = parse_args(argv)
    joke = build_joke()

    problems = check_joke(joke)
    if problems:
        for problem in problems:
            print(f"gate check failed: {problem}", file=sys.stderr)
        return 1

    if args.print:
        print(joke)

    output = args.output or os.environ.get("ENTRY_OUTPUT", DEFAULT_OUTPUT)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as handle:
        handle.write(joke + "\n")

    # Read the file back and verify it holds exactly the joke.
    with open(output, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != joke + "\n":
        print("read-back check failed: file does not match the joke",
              file=sys.stderr)
        return 1
    readback_problems = check_joke(written.strip())
    if readback_problems:
        for problem in readback_problems:
            print(f"read-back gate check failed: {problem}", file=sys.stderr)
        return 1

    print(f"wrote {len(joke.split())}-word joke to {output} "
          f"({len(joke)} chars, read-back verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
