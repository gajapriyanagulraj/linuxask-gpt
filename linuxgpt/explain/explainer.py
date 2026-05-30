from __future__ import annotations

from pathlib import Path

from linuxgpt.providers.llm import chat

_PROMPT = (Path(__file__).parent.parent / "prompts" / "explain.txt").read_text()


def explain_command(command: str) -> str:
    """Return a plain-English explanation of a bash command."""
    return chat(system=_PROMPT, user=command)
