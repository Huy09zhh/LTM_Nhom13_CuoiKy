import re
from pathlib import Path
from datetime import datetime


def safe_filename(name: str) -> str:
    name = name.replace("\\", "/").split("/")[-1]
    name = re.sub(r"[^\w.\- ()]+", "_", name)
    return name.strip() or "file"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def dated_dir(base: Path) -> Path:
    d = datetime.now().strftime("%Y-%m-%d")
    return base / d


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    i = 1
    while True:
        candidate = parent / f"{stem}_{i}{suffix}"
        if not candidate.exists():
            return candidate
        i += 1