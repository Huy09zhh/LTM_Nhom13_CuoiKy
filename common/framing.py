# common/framing.py
import json
import struct
import socket
from typing import Any, Dict


def send_json(sock: socket.socket, obj: Dict[str, Any]) -> None:
    """
    Send JSON with 4-byte big-endian length prefix.
    """
    data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
    header = struct.pack("!I", len(data))
    sock.sendall(header + data)


def recv_json(sock: socket.socket) -> Dict[str, Any]:
    """
    Receive JSON with 4-byte big-endian length prefix.
    """
    header = recvall(sock, 4)
    if not header:
        raise ConnectionError("Socket closed while reading header")
    (n,) = struct.unpack("!I", header)
    payload = recvall(sock, n)
    if payload is None:
        raise ConnectionError("Socket closed while reading payload")
    return json.loads(payload.decode("utf-8"))


def recvall(sock: socket.socket, n: int) -> bytes:
    """
    Read exactly n bytes or raise ConnectionError.
    """
    buf = bytearray()
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("Socket closed during recvall")
        buf.extend(chunk)
    return bytes(buf)
