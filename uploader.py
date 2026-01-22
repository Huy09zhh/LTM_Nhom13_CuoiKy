# client/uploader.py
import socket
import os
import sys
from pathlib import Path
from typing import List

# add project root so we can import common/*
ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from common.framing import send_json, recv_json


def upload_files(host: str, port: int, files: List[Path]) -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    client_id = os.getenv("USERNAME") or os.getenv("USER") or "client"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        send_json(s, {"client_id": client_id})
        print(recv_json(s))

        send_json(s, {"files": [{"name": f.name, "size": f.stat().st_size} for f in files]})

        for f in files:
            ack = recv_json(s)
            if not ack.get("ok"):
                print("Server refused:", ack)
                return

            show_name = ack.get("name", f.name)
            total = f.stat().st_size
            sent = 0
            last_percent = -1

            print(f"Uploading {show_name}: 0%", end="", flush=True)

            with open(f, "rb") as fp:
                while True:
                    chunk = fp.read(65536)
                    if not chunk:
                        break
                    s.sendall(chunk)
                    sent += len(chunk)
                    percent = (sent * 100 // total) if total > 0 else 100

                    # chỉ update khi tăng mỗi 10%
                    step = 10
                    p_show = (percent // step) * step
                    if p_show != last_percent or percent == 100:
                        print(f"\rUploading {show_name}: {p_show}%", end="", flush=True)
                        last_percent = p_show

            print()

        final = recv_json(s)

        if not final.get("ok"):
            print("Upload failed.")
            if final.get("error"):
                print("Error:", final["error"])
            return

        results = final.get("results", [])
        ok_names = [r.get("name") for r in results if r.get("ok")]

        print("Uploaded:")
        for n in ok_names:
            print(f" - {n}")