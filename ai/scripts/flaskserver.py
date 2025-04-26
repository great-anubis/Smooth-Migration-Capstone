from flask import Flask, request, jsonify, abort
import os
import sys
import json


SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from questionnaire import collect_responses
from generate_prompt import build_prompt
from models.baseline_model import generate_recommendation

app = Flask(__name__)


checklist_data = {}

def run_ai_pipeline():
    
    user_data = collect_responses()

    
    prompt = build_prompt(user_data)

    
    raw_json = generate_recommendation(prompt)

    
    try:
        checklist = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print(" JSON parse error:", e)
        return {"error": "AI response was not valid JSON."}

    return checklist

@app.route("/recommendations", methods=["POST"])
def get_recommendations():
    checklist = run_ai_pipeline()

    if "tasks" not in checklist:
        return jsonify({"error": "Checklist not found in AI output."}), 400

    
    for i, item in enumerate(checklist["tasks"]):
        item["id"] = str(i)
        item["completed"] = False

    checklist_data["tasks"] = checklist["tasks"]

    return jsonify(checklist_data)

@app.route("/task/<task_id>", methods=["PATCH"])
def update_task_status(task_id):
    data = request.get_json()
    status = data.get("completed")

    if "tasks" not in checklist_data:
        return jsonify({"error": "Checklist not found"}), 404

    for task in checklist_data["tasks"]:
        if task["id"] == task_id:
            task["completed"] = bool(status)
            return jsonify({"message": "Task updated", "task": task}), 200

    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
