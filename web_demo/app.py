# web_demo/app.py
from pathlib import Path
import sys
from flask import Flask, render_template, request, jsonify
import subprocess
from pathlib import Path

app = Flask(__name__)
TMP = Path("web_upload_tmp")
TMP.mkdir(exist_ok=True)

SERVER_HOST = "127.0.0.1"
SERVER_PORT = "9009"

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/upload")
def upload():
    files = request.files.getlist("files")
    if not files:
        return jsonify({"ok": False, "error": "Bạn chưa chọn file."}), 400

    saved = []
    for f in files:
        name = f.filename.replace("\\", "/").split("/")[-1]
        path = TMP / name
        f.save(path)
        saved.append(str(path))

    ROOT = Path(__file__).resolve().parents[1]     # D:\UploadMultiFile2
    CLIENT_PY = ROOT / "client" / "client.py"

    cmd = [sys.executable, str(CLIENT_PY), SERVER_HOST, SERVER_PORT, *saved]

    p = subprocess.run(cmd, capture_output=True, text=True)

    if p.returncode != 0:
        return jsonify({"ok": False, "error": "client failed", "detail": p.stderr or p.stdout}), 500

    return jsonify({"ok": True, "msg": "Upload thành công!", "detail": p.stdout})

if __name__ == "__main__":
    app.run(debug=True)
