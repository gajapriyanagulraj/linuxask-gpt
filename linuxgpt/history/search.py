"""
History search — reads ~/.bash_history or ~/.zsh_history and uses the LLM
to pick the most relevant commands for a plain-English query.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from linuxgpt.providers.llm import chat

_SYSTEM = (
    "You are a bash history assistant. "
    "The user will give you a natural-language description and a list of recent commands. "
    "Return only the top matching commands, one per line, most relevant first. "
    "Output ONLY the raw commands — no numbering, no explanation."
)

_MAX_HISTORY_LINES = 500  # keep prompt size reasonable


def _read_history() -> list[str]:
    """Return deduplicated history lines from bash or zsh history."""
    candidates = [
        Path.home() / ".zsh_history",
        Path.home() / ".bash_history",
    ]
    lines: list[str] = []
    for path in candidates:
        if path.exists():
            raw = path.read_bytes().decode("utf-8", errors="replace")
            # zsh stores timestamps like `: 1234567890:0;command`
            for line in raw.splitlines():
                line = re.sub(r"^:\s*\d+:\d+;", "", line).strip()
                if line and not line.startswith("#"):
                    lines.append(line)
    # deduplicate while preserving order (most recent last → reverse for LLM)
    seen: set[str] = set()
    unique: list[str] = []
    for ln in reversed(lines):
        if ln not in seen:
            seen.add(ln)
            unique.append(ln)
    return unique[:_MAX_HISTORY_LINES]


def search_history(query: str, limit: int = 5) -> list[str]:
    """Return up to *limit* history commands relevant to the query."""
    history = _read_history()
    if not history:
        return []

    history_block = "\n".join(history)
    user_msg = (
        f"Query: {query}\n\n"
        f"History (most recent first):\n{history_block}\n\n"
        f"Return the {limit} most relevant commands."
    )
    raw = chat(system=_SYSTEM, user=user_msg)
    results = [ln.strip() for ln in raw.splitlines() if ln.strip()]
    return results[:limit]
