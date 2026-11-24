#!/usr/bin/env python3
"""Entry program for make.fun competition
u-kreutzx-the-funniest-out-of-office-054815cf.

Reads entry.txt from this repository, validates it against the
competition gate (a single line, 1 to 140 characters, not only
whitespace), and writes it byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.txt.
"""

import os
import sys

MAX_CHARS = 140


def main() -> int:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    with open(src, "rb") as f:
        raw = f.read()

    text = raw.decode("utf-8")  # gate: entry must be UTF-8 text

    # Normalize one trailing line ending (LF or CRLF); anything else
    # that looks like a second line is a gate failure.
    if text.endswith("\r\n"):
        text = text[:-2]
    elif text.endswith("\n"):
        text = text[:-1]

    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if any(ord(ch) < 0x20 and ch != "\t" for ch in text):
        print("entry contains control characters", file=sys.stderr)
        return 1

    line = text
    if not (1 <= len(line) <= MAX_CHARS):
        print(
            f"entry length {len(line)} outside gate 1..{MAX_CHARS}",
            file=sys.stderr,
        )
        return 1
    if not line.strip():
        print("entry must not be only whitespace", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(line.encode("utf-8"))
    # Round-trip check: what we wrote must be exactly the entry.
    with open(out_path, "rb") as f:
        if f.read().decode("utf-8") != line:
            print("round-trip mismatch on output", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
