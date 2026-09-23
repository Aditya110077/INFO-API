from flask import Flask, request, jsonify
from main import SiLeNt_KiLL, UNknown, full_json, LOGIN_UID, LOGIN_PW

app = Flask(__name__)


# ---------- HOME ----------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "usage":  "/aditya?uid=7021709939"
    })


# ---------- MAIN ROUTE ----------
@app.route("/aditya", methods=["GET"])
def aditya_player():
    uid = request.args.get("uid", "").strip()

    # Validate UID
    if not uid or not uid.isdigit():
        return jsonify({
            "success": False,
            "error":   "Valid numeric uid required"
        }), 400

    # Fetch from Free Fire
    try:
        data = SiLeNt_KiLL(uid, LOGIN_UID, LOGIN_PW)
    except Exception as e:
        return jsonify({
            "success": False,
            "error":   f"Request failed: {str(e)}"
        }), 500

    # Error handling
    if data.get("err"):
        return jsonify({
            "success": False,
            "error":   str(data["err"])
        }), 500

    if not data.get("jwt"):
        return jsonify({
            "success": False,
            "error":   "Token fetch failed"
        }), 401

    resp = data.get("resp")
    if resp is None:
        return jsonify({
            "success": False,
            "error":   "No response from Free Fire server"
        }), 502

    if resp.status_code != 200:
        return jsonify({
            "success": False,
            "error":   f"HTTP {resp.status_code}",
            "details": resp.text[:300]
        }), resp.status_code

    # Decrypt + Parse + Return full JSON
    try:
        dec = UNknown(resp.content)
        raw_json = full_json(dec)

        return jsonify({
            "success": True,
            "data":    raw_json
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error":   f"Parse failed: {str(e)}"
        }), 500


# ---------- RUN ----------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)