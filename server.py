import hmac
import os
from datetime import timedelta
from functools import wraps

import cloudinary
import cloudinary.api
import cloudinary.uploader
from flask import Flask, jsonify, redirect, render_template, request, session, url_for

APP_PASSWORD = os.environ.get("APP_PASSWORD", "")
CLOUDINARY_FOLDER = os.environ.get("CLOUDINARY_FOLDER", "fishing-map")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")
app.permanent_session_lifetime = timedelta(days=365)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25MB / 1枚

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
    secure=True,
)


def _cloudinary_configured():
    cfg = cloudinary.config()
    return bool(cfg.cloud_name and cfg.api_key and cfg.api_secret)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("authed"):
            if request.path.startswith("/api/"):
                return jsonify({"error": "unauthorized"}), 401
            return redirect(url_for("login", next=request.path))
        return view(*args, **kwargs)

    return wrapped


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        submitted = request.form.get("password", "")
        if APP_PASSWORD and hmac.compare_digest(submitted, APP_PASSWORD):
            session.permanent = True
            session["authed"] = True
            return redirect(request.args.get("next") or url_for("index"))
        error = "パスワードが違います"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def index():
    return render_template("map.html")


def _context_dict(resource):
    ctx = resource.get("context") or {}
    return ctx.get("custom", ctx)


def _resource_to_record(resource):
    ctx = _context_dict(resource)
    lat = ctx.get("lat")
    lon = ctx.get("lon")
    return {
        "key": resource["public_id"],
        "name": ctx.get("name", resource["public_id"]),
        "url": resource["secure_url"],
        "lat": float(lat) if lat not in (None, "") else None,
        "lon": float(lon) if lon not in (None, "") else None,
        "size": int(ctx["size"]) if ctx.get("size") else None,
        "takenAt": ctx.get("takenAt") or None,
        "title": ctx.get("title", ""),
    }


@app.route("/api/photos", methods=["GET"])
def list_photos():
    if not _cloudinary_configured():
        return jsonify({"error": "Cloudinaryの環境変数が未設定です"}), 500

    records = []
    next_cursor = None
    while True:
        resp = cloudinary.api.resources(
            type="upload",
            prefix=f"{CLOUDINARY_FOLDER}/",
            context=True,
            max_results=500,
            next_cursor=next_cursor,
        )
        records.extend(_resource_to_record(r) for r in resp.get("resources", []))
        next_cursor = resp.get("next_cursor")
        if not next_cursor:
            break
    return jsonify(records)


@app.route("/api/photos", methods=["POST"])
def upload_photo():
    if not _cloudinary_configured():
        return jsonify({"error": "Cloudinaryの環境変数が未設定です"}), 500

    file = request.files.get("file")
    if file is None:
        return jsonify({"error": "no file"}), 400

    lat = request.form.get("lat", "")
    lon = request.form.get("lon", "")
    taken_at = request.form.get("takenAt", "")
    title = request.form.get("title", "")
    name = request.form.get("name", file.filename or "")
    size = request.form.get("size", "")

    context = {
        "lat": lat,
        "lon": lon,
        "takenAt": taken_at,
        "title": title,
        "name": name,
        "size": size,
    }
    context = {k: v for k, v in context.items() if v not in (None, "")}

    result = cloudinary.uploader.upload(
        file,
        folder=CLOUDINARY_FOLDER,
        context=context,
        resource_type="image",
    )
    return jsonify(_resource_to_record(result))


@app.route("/api/photos/<path:public_id>", methods=["PATCH"])
def update_photo(public_id):
    data = request.get_json(silent=True) or {}
    title = data.get("title", "")
    cloudinary.uploader.add_context({"title": title}, [public_id])
    return jsonify({"ok": True})


@app.route("/api/photos/<path:public_id>", methods=["DELETE"])
def delete_photo(public_id):
    cloudinary.uploader.destroy(public_id)
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
