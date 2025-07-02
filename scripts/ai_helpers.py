"""Helper functions to interact with Gemini CLI non-interactively.

Relies on the `gemini` executable being available in PATH and a valid
GEMINI_API_KEY (or other supported auth) configured, as described in
https://github.com/google-gemini/gemini-cli.
"""
from __future__ import annotations

import os
import subprocess
import shutil
from pathlib import Path
from typing import Iterable, List


class GeminiCliError(RuntimeError):
    """Raised when the gemini CLI returns a non-zero status code."""


def ask_gemini(prompt: str, files: Iterable[Path] | None = None) -> str:
    """Send *prompt* to Gemini CLI, optionally attaching *files*.

    Parameters
    ----------
    prompt : str
        The prompt text.
    files : Iterable[Path] | None
        Optional file paths whose contents should be injected. Paths are
        validated before invocation. They are passed as positional
        arguments to `gemini`, which reads and injects them according to
        its default behaviour (similar to `@file` in interactive mode).
    Returns
    -------
    str
        The stdout produced by the gemini CLI (model response).
    """
    # Resolve path to gemini executable (.cmd on Windows via npm or binary on *nix)
    exe_path = os.environ.get("GEMINI_CLI_PATH") or shutil.which("gemini") or shutil.which("gemini.cmd")
    if exe_path is None:
        raise GeminiCliError(
            "gemini CLI não encontrado no PATH ou GEMINI_CLI_PATH. Siga https://github.com/google-gemini/gemini-cli#install."
        )

        # Build prompt with @file references so Gemini CLI loads the file content
    final_prompt = prompt
    validated_paths: List[str] = []
    if files:
        for f in files:
            path = Path(f).expanduser().resolve()
            if not path.is_file():
                raise FileNotFoundError(path)
            validated_paths.append(str(path))
    if validated_paths:
        final_prompt = f"{final_prompt} " + " ".join(f"@{p}" for p in validated_paths)

    cmd: List[str] = [exe_path, "--prompt", final_prompt]

    

    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)

    if proc.returncode != 0:
        raise GeminiCliError(proc.stderr.strip() or f"gemini retornou código {proc.returncode}")

    return proc.stdout.strip()
