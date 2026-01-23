import socket
import sys
from pathlib import Path
from typing import List, Dict, Any

def resolve_duplicate(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    i = 2
    while True:
        new_name = f"{stem} ({i}){suffix}"
        new_path = parent / new_name
        if not new_path.exists():
            return new_path
        i += 1

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from common.framing import recv_json, send_json
from common.protocol import recv_to_file

from config import STORAGE_DIR, MAX_FILE_SIZE
from file_utils import ensure_dir, dated_dir


def handle_client(conn: socket.socket, addr):
    try:
        hello = recv_json(conn)
        client_id = str(hello.get("client_id", "client"))
        send_json(conn, {"ok": True, "msg": "connected"})

        manifest = recv_json(conn)
        files: List[Dict[str, Any]] = manifest.get("files", [])

        base_dir = STORAGE_DIR / client_id
        day_dir = dated_dir(base_dir)
        ensure_dir(day_dir)

        results = []

        for f in files:
            raw_name = f.get("name", "file")
            size = int(f.get("size", 0))

            name = raw_name.replace("\\", "/").split("/")[-1]

            if size <= 0 or size > MAX_FILE_SIZE:
                send_json(conn, {
                    "ok": False,
                    "error": "Invalid file size",
                    "name": name
                })
                results.append({"name": name, "ok": False})
                return

            out_path = day_dir / name
            out_path = resolve_duplicate(out_path)

            final_name = out_path.name

            send_json(conn, {"ok": True, "name": final_name})

            with open(out_path, "wb") as fp:
                recv_to_file(conn, fp, size)

            results.append({"name": name, "ok": True})

        send_json(conn, {"ok": True, "results": results})

    except Exception as e:
        try:
            send_json(conn, {"ok": False, "error": str(e)})
        except Exception:
            pass
    finally:
        try:
            conn.close()
        except Exception:
            pass