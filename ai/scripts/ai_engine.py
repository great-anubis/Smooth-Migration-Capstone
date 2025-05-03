import argparse
import os
import json
import sys

SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from questionnaire import collect_responses
from generate_prompt import build_prompt
from models.baseline_model import generate_recommendation

REQUIRED_KEYS = ['task', 'phase', 'api_trigger']

def fill_missing_fields(task):
    if 'task' not in task or not task['task']:
        task['task'] = "Unknown Task"
    if 'phase' not in task or not task['phase']:
        task['phase'] = "Unassigned"
    if 'api_trigger' not in task or not task['api_trigger']:
        task['api_trigger'] = "unknown"
    if 'due_date' not in task:
        task['due_date'] = None
    if 'completed' not in task:
        task['completed'] = False
    return task

def main():
    parser = argparse.ArgumentParser(description="AI Migration Checklist Debug CLI")
    parser.add_argument("--user_data", type=str, help="Path to user_data JSON file (optional)")
    parser.add_argument("--from_stdin", action='store_true', help="Read user data from stdin as JSON")
    args = parser.parse_args()

    try:
        if args.from_stdin:
            user_data = json.load(sys.stdin)

            # 🛠️ Patch: Adapt flat input (from FlutterFlow) into Q&A format
            if isinstance(user_data, dict) and all(isinstance(v, (str, int, float, bool)) for v in user_data.values()):
                user_data = {
                    "Basic Info": [
                        { "question": k.replace("_", " ").capitalize(), "answer": str(v) }
                        for k, v in user_data.items()
                    ]
                }

        elif args.user_data and os.path.exists(args.user_data):
            with open(args.user_data, "r") as f:
                user_data = json.load(f)
        else:
            user_data = collect_responses()
    except Exception as e:
        print("ERROR: Failed to load user data:", e)
        return

    try:
        prompt = build_prompt(user_data)
    except Exception as e:
        print("ERROR: Failed to build prompt:", e)
        return

    try:
        raw_json = generate_recommendation(prompt)
    except Exception as e:
        print("ERROR: Model/API call failed:", e)
        return

    try:
        checklist = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print("ERROR: Failed to parse JSON:", e)
        print("Raw output was:\n", raw_json)
        return

    for section in ["Pre-Departure", "Departure", "Post-Departure"]:
        if section in checklist and isinstance(checklist[section], list):
            checklist[section] = [fill_missing_fields(task) for task in checklist[section]]

    print(json.dumps(checklist, indent=4))

if __name__ == "__main__":
    main()
