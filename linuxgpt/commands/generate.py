from __future__ import annotations

import re
from pathlib import Path

from linuxgpt.providers.llm import chat

_PROMPT = (Path(__file__).parent.parent / "prompts" / "generate.txt").read_text()


def generate_command(description: str) -> str:
    """Convert a plain-English description into a bash command."""
    raw = chat(system=_PROMPT, user=description)
    return _sanitize(raw)


def _sanitize(cmd: str) -> str:
    """Strip markdown fences and stray backticks the LLM sometimes adds."""
    cmd = cmd.strip()
    # remove ```bash ... ``` or ``` ... ```
    fenced = re.match(r"^```(?:bash|sh)?\n?(.*?)\n?```$", cmd, re.DOTALL)
    if fenced:
        return fenced.group(1).strip()
    # remove single surrounding backticks  `command`
    if cmd.startswith("`") and cmd.endswith("`"):
        cmd = cmd[1:-1]
    return cmd.strip()
