"""
linuxgpt CLI — Natural Language Interface for Linux
"""
from __future__ import annotations

import sys
import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from linuxgpt.commands.generate import generate_command
from linuxgpt.explain.explainer import explain_command
from linuxgpt.commands.fix import fix_command
from linuxgpt.history.search import search_history

app = typer.Typer(
    name="linuxgpt",
    help="Natural Language Interface for Linux — commands without memorization.",
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()


# ──────────────────────────────────────────────
# Default: generate a command from plain English
# ──────────────────────────────────────────────
@app.command(name="ask", help="[bold]Generate[/bold] a Linux command from plain English.")
def ask(
    description: str = typer.Argument(..., help="What you want to do in plain English."),
    run: bool = typer.Option(False, "--run", "-r", help="Execute the command after generating."),
):
    with console.status("[cyan]Thinking…[/cyan]", spinner="dots"):
        cmd = generate_command(description)

    _print_command(cmd)

    if run:
        _confirm_and_run(cmd)


# ──────────────────────────────────────────────
# linuxgpt explain "<cmd>"
# ──────────────────────────────────────────────
@app.command(name="explain", help="[bold]Explain[/bold] what a Linux command does.")
def explain(
    command: str = typer.Argument(..., help="The Linux command to explain."),
):
    with console.status("[cyan]Explaining…[/cyan]", spinner="dots"):
        text = explain_command(command)

    console.print(Panel(text, title="[bold green]Explanation[/bold green]", border_style="green"))


# ──────────────────────────────────────────────
# linuxgpt fix "<error message>"
# ──────────────────────────────────────────────
@app.command(name="fix", help="[bold]Fix[/bold] a failed command or error message.")
def fix(
    error: str = typer.Argument(..., help="The error message or failed command."),
):
    with console.status("[cyan]Finding fix…[/cyan]", spinner="dots"):
        suggestion = fix_command(error)

    _print_command(suggestion, title="Suggested Fix")


# ──────────────────────────────────────────────
# linuxgpt history "<query>"
# ──────────────────────────────────────────────
@app.command(name="history", help="[bold]Search[/bold] your bash/zsh history in plain English.")
def history(
    query: str = typer.Argument(..., help="What you remember about the command."),
    limit: int = typer.Option(5, "--limit", "-n", help="Max results to return."),
):
    with console.status("[cyan]Searching history…[/cyan]", spinner="dots"):
        results = search_history(query, limit=limit)

    if not results:
        console.print("[yellow]No matching commands found in history.[/yellow]")
        return

    console.print(Panel(
        "\n".join(f"[dim]{i+1}.[/dim] [bold cyan]{r}[/bold cyan]" for i, r in enumerate(results)),
        title="[bold]History Matches[/bold]",
        border_style="blue",
    ))


# ──────────────────────────────────────────────
# linuxgpt  (no sub-command → interactive REPL)
# ──────────────────────────────────────────────
@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        _interactive_mode()


def _interactive_mode():
    console.print(Panel(
        "[bold cyan]linuxgpt[/bold cyan] interactive mode\n"
        "[dim]Type your request in English. Commands: [bold]:exit[/bold] [bold]:help[/bold][/dim]",
        border_style="cyan",
    ))
    while True:
        try:
            text = console.input("[bold green]> [/bold green]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Bye![/dim]")
            sys.exit(0)

        if not text:
            continue
        if text.lower() in (":exit", ":quit", "exit", "quit"):
            console.print("[dim]Bye![/dim]")
            sys.exit(0)
        if text.lower() == ":help":
            console.print(
                "[bold]ask[/bold]      <description>   generate a command\n"
                "[bold]explain[/bold]  <command>        explain a command\n"
                "[bold]fix[/bold]      <error>          fix an error\n"
                "[bold]history[/bold]  <query>          search bash history\n"
                "[bold]:exit[/bold]                    quit"
            )
            continue

        with console.status("[cyan]Thinking…[/cyan]", spinner="dots"):
            cmd = generate_command(text)
        _print_command(cmd)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────
def _print_command(cmd: str, title: str = "Command"):
    syntax = Syntax(cmd, "bash", theme="monokai", word_wrap=True)
    console.print(Panel(syntax, title=f"[bold yellow]{title}[/bold yellow]", border_style="yellow"))


def _confirm_and_run(cmd: str):
    import subprocess
    confirmed = typer.confirm(f"Run: {cmd!r}?")
    if confirmed:
        result = subprocess.run(cmd, shell=True, text=True)  # noqa: S602
        if result.returncode != 0:
            console.print(f"[red]Exited with code {result.returncode}[/red]")
