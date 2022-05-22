from pathlib import Path


def get_base_dir() -> Path:
    return Path(__file__).resolve().parent.parent
