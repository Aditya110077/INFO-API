from flask import Flask, request, jsonify
from main import SiLeNt_KiLL, UNknown, full_json, REGION_SERVERS

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "usage":  "/aditya?uid=7021709939&region=IND",
        "regions": list(REGION_SERVERS.keys())
    })


@app.route("/aditya", methods=["GET"])
def aditya_player():
    uid    = request.args.get("uid", "").strip()
    region = request.args.get("region", "IND").strip().upper()

    if not uid or not uid.isdigit():
        return jsonify({"success": False, "error": "Valid numeric uid required"}), 400

    if region not in REGION_SERVERS:
        return jsonify({
            "success": False,
            "error":   f"Unsupported region. Use: {list(REGION_SERVERS.keys())}"
        }), 400

    try:
        data = SiLeNt_KiLL(uid, region=region)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    if data.get("err"):
        return jsonify({"success": False, "error": str(data["err"])}), 500
    if not data.get("jwt"):
        return jsonify({"success": False, "error": "Token fetch failed"}), 401

    resp = data.get("resp")
    if resp is None:
        return jsonify({"success": False, "error": "No response"}), 502
    if resp.status_code != 200:
        return jsonify({"success": False, "error": f"HTTP {resp.status_code}"}), resp.status_code

    try:
        dec = UNknown(resp.content)
        raw_json = full_json(dec)
        basic = raw_json.get("basic_info", {}) or {}

        return jsonify({
            "success": True,
            "uid":     str(basic.get("account_id", uid)),
            "name":    basic.get("nickname"),
            "level":   basic.get("level"),
            "region":  basic.get("region"),
            "data":    raw_json
        }), 200

    except Exception as e:
        return jsonify({"success": False, "error": f"Parse failed: {e}"}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)