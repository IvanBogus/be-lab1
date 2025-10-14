from datetime import datetime, timezone
from flask import jsonify
from . import app

@app.get("/healthcheck")
def healthcheck():
    return jsonify({
        "date": datetime.now(timezone.utc).isoformat(),
        "status": "ok"
    }), 200

@app.get("/")
def hello():
    return jsonify({"message": "Hi from Lab1 via Docker!"})
