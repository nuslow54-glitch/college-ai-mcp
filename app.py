from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyEN2rj_WGPKqzew0GuJbogrS4BWt1OPfVfZTIdl7rIUCI7cJS2CZh8sIuC1vH7Smc96w/exec"


@app.route("/")
def home():
    return "College AI Server is running"


@app.route("/college_search")
def college_search():
    keyword = request.args.get("keyword", "").strip()

    if not keyword:
        return jsonify({
            "success": False,
            "message": "กรุณาระบุ keyword"
        })

    try:
        response = requests.get(
            GOOGLE_SCRIPT_URL,
            params={"q": keyword},
            timeout=15
        )

        data = response.json()

        return jsonify({
            "success": True,
            "keyword": keyword,
            "data": data.get("results", [])
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
