#!/usr/bin/env python3
"""Expose the user's PStack model choices to Codex at task start."""

import os
from pathlib import Path


def main() -> None:
    codex_home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser()
    model_map = codex_home / "pstack-models.md"

    try:
        choices = model_map.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return

    if choices:
        print(
            "PStack model choices for this task. Apply these per-role defaults "
            "when using PStack skills and subagents; explicit user instructions "
            "take precedence.\n"
        )
        print(choices)


if __name__ == "__main__":
    main()
