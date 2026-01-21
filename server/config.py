from pathlib import Path

HOST = "0.0.0.0"
PORT = 9009

MAX_FILE_SIZE = 200 * 1024 * 1024

STORAGE_DIR = Path(__file__).resolve().parent / "storage"