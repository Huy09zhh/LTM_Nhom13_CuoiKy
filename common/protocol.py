# common/protocol.py
from typing import BinaryIO
import socket

from .framing import send_json, recv_json


def recv_to_file(sock: socket.socket, out_fp: BinaryIO, size: int, chunk_size: int = 65536) -> None:
    """
    Receive exactly `size` bytes from socket and write to out_fp.
    """
    remaining = size
    while remaining > 0:
        chunk = sock.recv(min(chunk_size, remaining))
        if not chunk:
            raise ConnectionError("Socket closed while receiving file bytes")
        out_fp.write(chunk)
        remaining -= len(chunk)
        