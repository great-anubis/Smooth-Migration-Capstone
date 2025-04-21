from flask import Flask, request, jsonify
import sys
import os
import json

# Add project root to import path
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import your internal logic
from scripts.generate_prompt import build_prompt
from models.baseline_model import generate_recommendation

app = Flask(__name__)

@app.route("/recommendations", methods=["POST"])
def get_recommendation():
    try:
        user_data = request.json  # Expecting user answers in JSON
        prompt = build_prompt(user_data)
        raw_output = generate_recommendation(prompt)

        try:
            checklist = json.loads(raw_output)
        except json.JSONDecodeError:
            checklist = {"raw_response": raw_output}

        return jsonify({"checklist": checklist})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

