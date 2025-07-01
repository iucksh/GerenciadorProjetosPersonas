"""Utility helpers for WindSurf adapter and CLI.

Guarantees safe execution of existing project scripts within project scope.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

ALLOWED_SCRIPTS = {
    "monitor": "monitor.py",
    "rotate": "rotate_personas.py",
    "report": "generate_report.py",
    "task_manager": "task_manager.py",
}

class ScriptExecutionError(RuntimeError):
    """Raised when an underlying script fails."""


def _get_script_path(key: str) -> Path:
    if key not in ALLOWED_SCRIPTS:
        raise ValueError(f"Script '{key}' is not in allowed list.")
    script_path = SCRIPTS_DIR / ALLOWED_SCRIPTS[key]
    if not script_path.exists():
        raise FileNotFoundError(script_path)
    return script_path


def run_script(key: str, *args: str, check: bool = True) -> Tuple[int, str, str]:
    """Run an allowed project script and return (returncode, stdout, stderr)."""
    script_path = _get_script_path(key)
    cmd: List[str] = [sys.executable, str(script_path), *args]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if check and proc.returncode != 0:
        raise ScriptExecutionError(proc.stderr.strip())
    return proc.returncode, proc.stdout, proc.stderr


def rotation_needed() -> bool:
    """Return True if the monitor output indicates rotation is required."""
    _code, out, _err = run_script("monitor", check=False)
    return "ALTERAÇÃO DE PERSONAS NECESSÁRIA" in out or "ALTERNACAO" in out  # fallback for possible accent stripping
