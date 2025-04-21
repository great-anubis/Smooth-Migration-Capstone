# app.py

from flask import Flask, request, jsonify
from scripts.ai_engine import get_recommendation_from_questionnaire
from dotenv import load_dotenv
import os


load_dotenv(dotenv_path="env/.env")

app = Flask(__name__)

@app.route("/recommendations", methods=["POST"])
def generate_recommendations():
    try:
        user_data = request.json
        ai_response = get_recommendation_from_questionnaire(user_data)
        return jsonify({"recommendation": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
