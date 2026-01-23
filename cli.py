# client/cli.py
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Args:
    host: str
    port: int
    files: List[Path]


def parse_args(argv: List[str]) -> Args:
    if len(argv) < 4:
        raise SystemExit("Usage: py client.py <host> <port> <file1> <file2> ...")

    host = argv[1]
    port = int(argv[2])

    files: List[Path] = []
    for p in argv[3:]:
        fp = Path(p)
        if fp.exists() and fp.is_file():
            files.append(fp)
        else:
            print(f"[CLIENT] Skip: {fp}")

    if not files:
        raise SystemExit("[CLIENT] No valid files.")

    return Args(host=host, port=port, files=files)
