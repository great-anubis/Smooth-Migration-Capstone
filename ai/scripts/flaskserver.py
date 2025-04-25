from flask import Flask, request, jsonify
from ai_engine import main as run_ai_engine

app = Flask(__name__)

@app.route("/recommendations", methods=["POST"])
def recommendations():
    try:
        result = run_ai_engine()
        return jsonify({"recommendations": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
