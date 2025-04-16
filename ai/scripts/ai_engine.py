import os
import json
import sys
SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from questionnaire import collect_responses
from generate_prompt import build_prompt
from models.baseline_model import generate_recommendation  # adjust import path if needed

def main():
    # 1. Collect user answers
    user_data = collect_responses()

    # 2. Turn answers into a single prompt string
    prompt = build_prompt(user_data)

    # 3. Call your baseline model to get a raw JSON string
    raw_json = generate_recommendation(prompt)

    # 4. Parse into a Python dict
    try:
        checklist = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print("❌ Failed to parse JSON:", e)
        print("Raw output was:\n", raw_json)
        return

    # 5. Print the final checklist
    print("\n✅ Final Migration Checklist:\n")
    print(json.dumps(checklist, indent=4))

if __name__ == "__main__":
    main()
