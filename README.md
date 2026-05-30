# linuxgpt

> **Natural Language Interface for Linux** — Linux commands without memorization.

```bash
linuxgpt ask "find files larger than 1GB"
# find / -type f -size +1G
```

---

## Features

| Sub-command | What it does |
|---|---|
| `ask "<description>"` | Generate a bash command from plain English |
| `explain "<command>"` | Explain what a command does, flag by flag |
| `fix "<error>"` | Suggest a fix for a failed command or error message |
| `history "<query>"` | Search your bash/zsh history in plain English |
| *(no args)* | Launch interactive REPL mode |

---

## Quick Start

### 1. Install

```bash
git clone https://github.com/your-username/linuxgpt
cd linuxgpt
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

### 2. Configure

```bash
cp .env.example .env
# edit .env — set your provider, model, and API key
```

#### Ollama (default, local, free)
```bash
# Install Ollama: https://ollama.com
ollama pull llama3.2
# .env stays as-is
```

#### OpenAI
```env
LINUXGPT_PROVIDER=openai
LINUXGPT_MODEL=gpt-4o-mini
LINUXGPT_BASE_URL=https://api.openai.com/v1
LINUXGPT_API_KEY=sk-...
```

#### Groq (fast + free tier)
```env
LINUXGPT_PROVIDER=groq
LINUXGPT_MODEL=llama3-8b-8192
LINUXGPT_BASE_URL=https://api.groq.com/openai/v1
LINUXGPT_API_KEY=gsk_...
```

---

## Usage

```bash
# Generate
linuxgpt ask "show listening ports"
# ss -tulpn

linuxgpt ask "show processes using most memory"
# ps aux --sort=-rss | head

linuxgpt ask "find files larger than 1GB"
# find / -type f -size +1G

# Generate & run immediately
linuxgpt ask "show disk usage by directory" --run

# Explain
linuxgpt explain "find . -name '*.log' -mtime +7 -delete"

# Fix
linuxgpt fix "permission denied when running rm file"
# sudo rm file

# History search
linuxgpt history "command I used to check open ports last week"

# Interactive REPL
linuxgpt
```

---

## Project Layout

```
linuxgpt/
├── cli.py              ← Typer CLI (entry point)
├── providers/
│   └── llm.py          ← OpenAI-compatible client (Ollama / OpenAI / Groq)
├── prompts/
│   ├── generate.txt    ← System prompt for command generation
│   ├── explain.txt     ← System prompt for explanation
│   └── fix.txt         ← System prompt for error fixing
├── commands/
│   ├── generate.py
│   └── fix.py
├── explain/
│   └── explainer.py
└── history/
    └── search.py
```

---

## Tech Stack

- **Python 3.10+**
- **Typer** — CLI framework
- **Rich** — beautiful terminal output
- **openai** SDK — works with Ollama, OpenAI, Groq, and any OpenAI-compatible endpoint

---

## License

MIT
