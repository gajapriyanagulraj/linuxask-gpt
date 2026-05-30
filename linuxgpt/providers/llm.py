"""
Provider abstraction — supports Ollama, OpenAI, and any OpenAI-compatible API.
Configure via environment variables or a .env file.
"""
from __future__ import annotations

import os
from functools import lru_cache

from openai import OpenAI


@lru_cache(maxsize=1)
def get_client() -> OpenAI:
    """Return a configured OpenAI-compatible client."""
    _load_dotenv()
    base_url = os.getenv("LINUXGPT_BASE_URL", "http://localhost:11434/v1")
    api_key = os.getenv("LINUXGPT_API_KEY", "ollama")  # Ollama ignores the key
    return OpenAI(base_url=base_url, api_key=api_key)


def get_model() -> str:
    _load_dotenv()
    return os.getenv("LINUXGPT_MODEL", "llama3.2")


def chat(system: str, user: str) -> str:
    """Send a single-turn chat request and return the text response."""
    client = get_client()
    model = get_model()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.1,
        max_tokens=512,
    )
    return (response.choices[0].message.content or "").strip()


def _load_dotenv():
    """Minimal .env loader — avoids a dependency on python-dotenv."""
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    env_path = os.path.abspath(env_path)
    if not os.path.isfile(env_path):
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)
