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
    """Ensure every task has required keys and optional fields with defaults."""
    # Required fields
    if 'task' not in task or not task['task']:
        task['task'] = "Unknown Task"
    if 'phase' not in task or not task['phase']:
        task['phase'] = "Unassigned"
    if 'api_trigger' not in task or not task['api_trigger']:
        task['api_trigger'] = "unknown"

    # Optional fields (enriched)
    if 'due_date' not in task:
        task['due_date'] = None  # Or "" if you prefer an empty string
    if 'completed' not in task:
        task['completed'] = False

    return task


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI Migration Checklist Debug CLI")
    parser.add_argument("--user_data", type=str, help="Path to user_data JSON file (optional)")
    parser.add_argument("--from_stdin", action='store_true', help="Read user data from stdin as JSON")
    args = parser.parse_args()

    if args.from_stdin:
        # Read JSON from stdin
        user_data = json.load(sys.stdin)
    elif args.user_data and os.path.exists(args.user_data):
        with open(args.user_data, "r") as f:
            user_data = json.load(f)
    else:
        user_data = collect_responses()

    prompt = build_prompt(user_data)

    try:
        raw_json = generate_recommendation(prompt)
    except Exception as e:
        print("❌ Model/API call failed:", e)
        return

    try:
        checklist = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print("❌ Failed to parse JSON:", e)
        print("Raw output was:\n", raw_json)
        return

    for section in ["Pre-Departure", "Departure", "Post-Departure"]:
        if section in checklist and isinstance(checklist[section], list):
            checklist[section] = [fill_missing_fields(task) for task in checklist[section]]

    print(json.dumps(checklist, indent=4))

if __name__ == "__main__":
    main()
