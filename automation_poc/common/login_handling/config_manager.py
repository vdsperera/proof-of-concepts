from pathlib import Path
import json
from typing import Dict

def get_config() -> Dict[str, str]:
    """Load config.json from this folder and validate required keys."""
    config_path = Path(__file__).parent / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Config not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        cfg = json.load(f)
    required = ("email", "password", "totp_secret")
    missing = [k for k in required if k not in cfg or not cfg[k]]
    if missing:
        raise ValueError(f"Missing config keys: {missing}")
    return {"email": cfg["email"], "password": cfg["password"], "totp_secret": cfg["totp_secret"]}