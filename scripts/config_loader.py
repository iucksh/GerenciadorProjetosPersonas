"""Config loader that merges `config.yaml` with sensible defaults.
Other scripts can import `get_config()` instead of opening YAML directly.
"""
from __future__ import annotations

import yaml
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_YAML = PROJECT_ROOT / "config.yaml"

DEFAULTS: Dict[str, Any] = {
    "rotation_interval": 900,
    "report_interval": 1800,
    "logging_level": "INFO",
    "reports_dir": "scripts/reports",
}


def get_config() -> Dict[str, Any]:
    data: Dict[str, Any] = DEFAULTS.copy()
    if CONFIG_YAML.exists():
        with CONFIG_YAML.open("r", encoding="utf-8") as f:
            yaml_data = yaml.safe_load(f) or {}
            data.update({k: v for k, v in yaml_data.items() if v is not None})
    return data


def main() -> None:  # simple debug helper
    import json
    print(json.dumps(get_config(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
