"""GPP – Command-line interface for Gerenciador de Projetos e Personas.

Usage examples:

    # Exibir status via monitor
    python scripts/cli.py monitor

    # Rotacionar personas (se necessário ou com --force)
    python scripts/cli.py rotate --force

    # Gerar relatórios
    python scripts/cli.py report

The CLI wraps existing project scripts via adapter_utils ensuring that
only whitelisted commands are executed.
"""
from __future__ import annotations

import sys
from typing import List
from pathlib import Path
import os
import platform

import typer
from rich.console import Console
from rich.panel import Panel

try:
    from .adapter_utils import run_script, rotation_needed
    from .ai_helpers import ask_gemini
except ImportError:
    # Fallback when executed as a standalone script (python scripts/cli.py)
    import pathlib, sys as _sys
    _PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
    if str(_PROJECT_ROOT) not in _sys.path:
        _sys.path.insert(0, str(_PROJECT_ROOT))
    from scripts.adapter_utils import run_script, rotation_needed
    from scripts.ai_helpers import ask_gemini

app = typer.Typer(name="gpp", add_completion=True, help="Gerenciador de Projetos & Personas + AI")
# Garantir encoding UTF-8 no Windows para evitar caracteres quebrados
if platform.system() == "Windows":
    # Alterar code-page da sessão; ignora erros caso falhe
    try:
        os.system("chcp 65001 >nul")
    except Exception:
        pass

console = Console(encoding="utf-8", force_terminal=True)


@app.command()
def monitor() -> None:
    """Execute monitor.py e exiba a saída."""
    _print_panel("Executando monitor.py…")
    _show_output(*run_script("monitor", check=False))


@app.command()
def rotate(force: bool = typer.Option(False, "--force", help="Ignorar verificação de necessidade e rotacionar mesmo assim")) -> None:
    """Rotacionar personas se necessário ou se --force for usado."""
    if not force and not rotation_needed():
        console.print("[yellow]Rotação não necessária de acordo com monitor.")
        raise typer.Exit(code=0)
    _print_panel("Executando rotate_personas.py…")
    _show_output(*run_script("rotate", check=False))


@app.command()
def report() -> None:
    """Gerar relatórios de progresso das personas ativas."""
    _print_panel("Executando generate_report.py…")
    _show_output(*run_script("report", check=False))


@app.command(name="run")
def run_script_cmd(
    script_name: str = typer.Argument(..., help="Nome lógico do script (monitor, rotate, report, task_manager)"),
    args: List[str] = typer.Argument(None, help="Argumentos adicionais a serem passados ao script"),
) -> None:
    """Executar um script permitido, passando argumentos literal."""
    _print_panel(f"Executando {script_name}…")
    _show_output(*run_script(script_name, *args, check=False))


def _show_output(rc: int, out: str, err: str) -> None:
    if out:
        console.print(Panel.fit(out, title="stdout", style="green"))
    if err:
        console.print(Panel.fit(err, title="stderr", style="red"))
    console.print(f"[bold]Return code:[/bold] {rc}")
    if rc != 0:
        sys.exit(rc)


def _print_panel(msg: str):
    console.print(Panel.fit(msg, style="cyan"))


@app.command()
def ai(
    prompt: str = typer.Argument(..., help="Texto do prompt a ser enviado ao Gemini"),
    file: List[Path] = typer.Option(None, "--file", "-f", help="Arquivos opcionais para enviar ao Gemini"),
) -> None:
    """Enviar prompt ao Gemini CLI, opcionalmente anexando arquivos."""
    _print_panel("🔮 Enviando prompt ao Gemini CLI…")
    try:
        output = ask_gemini(prompt, file)
        console.print(Panel.fit(output, title="Gemini", style="magenta"))
    except RuntimeError as exc:
        console.print(Panel.fit(str(exc), title="Erro", style="red"))


if __name__ == "__main__":
    app()
