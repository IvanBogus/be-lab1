# app/views.py
from datetime import datetime, timezone
from flask import jsonify, request
from . import app

# ---------- базові ендпоінти ----------
@app.get("/healthcheck")
def healthcheck():
    return jsonify({
        "date": datetime.now(timezone.utc).isoformat(),
        "status": "ok"
    }), 200


@app.get("/")
def hello():
    return jsonify({"message": "Expenses API (Lab2)"}), 200


# ---------- просте ін-меморі "сховище" ----------
db = {
    "users": {},        # id -> {id, name}
    "categories": {},   # id -> {id, title}
    "records": {}       # id -> {id, user_id, category_id, created_at, amount}
}
seq = {"users": 0, "categories": 0, "records": 0}


def next_id(kind: str) -> int:
    seq[kind] += 1
    return seq[kind]


# =============== USERS =================
@app.post("/user")
def create_user():
    payload = request.get_json(force=True, silent=True) or {}
    name = (payload.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    uid = next_id("users")
    user = {"id": uid, "name": name}
    db["users"][uid] = user
    return jsonify(user), 201


@app.get("/user/<int:user_id>")
def get_user(user_id: int):
    user = db["users"].get(user_id)
    if not user:
        return jsonify({"error": "user not found"}), 404
    return jsonify(user), 200


@app.delete("/user/<int:user_id>")
def delete_user(user_id: int):
    if user_id not in db["users"]:
        return jsonify({"error": "user not found"}), 404
    # каскадно прибираємо його записи
    for rid, rec in list(db["records"].items()):
        if rec["user_id"] == user_id:
            del db["records"][rid]
    del db["users"][user_id]
    return "", 204


@app.get("/users")
def list_users():
    return jsonify(list(db["users"].values())), 200


# ============= CATEGORIES ==============
@app.post("/category")
def create_category():
    payload = request.get_json(force=True, silent=True) or {}
    title = (payload.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    cid = next_id("categories")
    cat = {"id": cid, "title": title}
    db["categories"][cid] = cat
    return jsonify(cat), 201


@app.get("/category")
def list_categories():
    return jsonify(list(db["categories"].values())), 200


@app.delete("/category")
def delete_category():
    # видалення через query-параметр ?id=<int>
    raw = request.args.get("id")
    try:
        cid = int(raw)
    except (TypeError, ValueError):
        return jsonify({"error": "category id is required as query param ?id=<int>"}), 400

    if cid not in db["categories"]:
        return jsonify({"error": "category not found"}), 404

    # каскадно прибираємо записи цієї категорії
    for rid, rec in list(db["records"].items()):
        if rec["category_id"] == cid:
            del db["records"][rid]

    del db["categories"][cid]
    return "", 204


# ================ RECORDS ==============
@app.post("/record")
def create_record():
    payload = request.get_json(force=True, silent=True) or {}

    # валідація та приведення типів
    try:
        user_id = int(payload.get("user_id"))
        category_id = int(payload.get("category_id"))
        amount = float(payload.get("amount"))
    except (TypeError, ValueError):
        return jsonify({"error": "user_id, category_id and amount are required"}), 400

    if user_id not in db["users"]:
        return jsonify({"error": "user not found"}), 404
    if category_id not in db["categories"]:
        return jsonify({"error": "category not found"}), 404

    rid = next_id("records")
    rec = {
        "id": rid,
        "user_id": user_id,
        "category_id": category_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "amount": amount
    }
    db["records"][rid] = rec
    return jsonify(rec), 201


@app.get("/record/<int:record_id>")
def get_record(record_id: int):
    rec = db["records"].get(record_id)
    if not rec:
        return jsonify({"error": "record not found"}), 404
    return jsonify(rec), 200


@app.delete("/record/<int:record_id>")
def delete_record(record_id: int):
    if record_id not in db["records"]:
        return jsonify({"error": "record not found"}), 404
    del db["records"][record_id]
    return "", 204


@app.get("/record")
def list_records():
    """
    Фільтр за ?user_id=<int> і/або ?category_id=<int>.
    Хоч один із параметрів обов’язковий; без них — 400.
    """
    uid_raw = request.args.get("user_id")
    cid_raw = request.args.get("category_id")

    if uid_raw is None and cid_raw is None:
        return jsonify({"error": "At least one of user_id or category_id is required"}), 400

    def ok(rec):
        ok_ = True
        if uid_raw is not None:
            try:
                ok_ = ok_ and (rec["user_id"] == int(uid_raw))
            except ValueError:
                return False
        if cid_raw is not None:
            try:
                ok_ = ok_ and (rec["category_id"] == int(cid_raw))
            except ValueError:
                return False
        return ok_

    return jsonify([r for r in db["records"].values() if ok(r)]), 200
