# ai/src/app/api.py

import os
import sys
import json
from flask import Flask, request, jsonify

# ── Ensure project root is on path ────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# ────────────────────────────────────────────────────────────────────────────────

from scripts.generate_prompt import build_prompt
from models.baseline_model import generate_recommendation  # or from scripts.ai_engine import generate_recommendation

app = Flask(__name__)

# ── Load your mapping file ONCE ────────────────────────────────────────────────
MAPPING_PATH = os.path.join(PROJECT_ROOT, "scripts", "checklist_mapping.json")
try:
    with open(MAPPING_PATH, "r", encoding="utf-8") as f:
        api_mapping = json.load(f)
except Exception as e:
    print(f"⚠️  Could not load mapping file at {MAPPING_PATH}: {e}")
    api_mapping = {}
# ────────────────────────────────────────────────────────────────────────────────

@app.route("/recommendations", methods=["POST"])
def recommendations():
    user_data = request.get_json(force=True)
    if not isinstance(user_data, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    # 1. Build the LLM prompt
    prompt = build_prompt(user_data)

    # 2. Call your model
    raw = generate_recommendation(prompt)

    # 3. Parse JSON
    try:
        checklist = json.loads(raw)
    except json.JSONDecodeError as e:
        return jsonify({
            "error": "Failed to parse model output as JSON",
            "raw_output": raw,
            "parse_error": str(e)
        }), 500

    # 4. Enrich each task: infer trigger if missing, then attach endpoint
    for phase, tasks in checklist.items():
        for task in tasks:
            # 4a) Infer api_trigger if missing or unknown
            trigger = task.get("api_trigger")
            if not trigger or trigger not in api_mapping:
                desc = task.get("task", "").lower()
                for key, info in api_mapping.items():
                    for kw in info.get("trigger_keywords", []):
                        if kw.lower() in desc:
                            trigger = key
                            task["api_trigger"] = key
                            break
                    if task.get("api_trigger"):
                        break

            # 4b) Attach the real endpoint (or None if still missing)
            mapping_info = api_mapping.get(task.get("api_trigger"), {})
            task["api_endpoint"] = mapping_info.get("api_endpoint")

    # 5. Return the enriched checklist
    return jsonify(checklist), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
