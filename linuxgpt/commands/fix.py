from __future__ import annotations

from pathlib import Path

from linuxgpt.providers.llm import chat
from linuxgpt.commands.generate import _sanitize

_PROMPT = (Path(__file__).parent.parent / "prompts" / "fix.txt").read_text()


def fix_command(error: str) -> str:
    """Suggest a fix for a failed command or error message."""
    raw = chat(system=_PROMPT, user=error)
    return _sanitize(raw)
