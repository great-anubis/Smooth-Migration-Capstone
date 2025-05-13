import argparse
import os
import json
import sys

SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from questionnaire import (
    get_basic_info_questions,
    get_pre_departure_questions,
    get_departure_questions,
    get_housing_preferences_questions,
    get_job_financial_questions,
    get_healthcare_insurance_questions,
    get_legal_documentation_questions,
    get_post_arrival_questions
)
from generate_prompt import build_prompt
from models.baseline_model import generate_recommendation

REQUIRED_KEYS = ['task', 'phase', 'api_trigger']

# Utility to fill missing keys in each task

def fill_missing_fields(task):
    task.setdefault('task', 'Unknown Task')
    task.setdefault('phase', 'Unassigned')
    task.setdefault('api_trigger', 'unknown')
    task.setdefault('due_date', None)
    task.setdefault('completed', False)
    return task

# Sections mapping for interactive prompts
SECTIONS = {
    "Basic Info": get_basic_info_questions,
    "Pre-Departure": get_pre_departure_questions,
    "Departure": get_departure_questions,
    "Housing Preferences": get_housing_preferences_questions,
    "Job & Financial": get_job_financial_questions,
    "Healthcare & Insurance": get_healthcare_insurance_questions,
    "Legal Documentation": get_legal_documentation_questions,
    "Post-Arrival": get_post_arrival_questions
}

# Interactive data collection

def collect_interactive_data():
    print("\nPlease answer the following questions. Press Enter after each answer.\n")
    data = {}
    for section, func in SECTIONS.items():
        print(f"--- {section} ---")
        answers = []
        for q in func():
            ans = input(q + " ")
            answers.append({"question": q, "answer": ans.strip()})
        data[section] = answers
    return data


def main():
    parser = argparse.ArgumentParser(description="AI Migration Checklist CLI")
    parser.add_argument("--user_data", type=str, help="Path to user_data JSON file (optional)")
    parser.add_argument("--from_stdin", action='store_true', help="Read user data from stdin as JSON")
    args = parser.parse_args()

    # Determine data source: stdin, file, or interactive
    if args.from_stdin:
        user_data = json.load(sys.stdin)
    elif args.user_data:
        if os.path.exists(args.user_data):
            with open(args.user_data) as f:
                user_data = json.load(f)
        else:
            print(f"ERROR: File not found: {args.user_data}")
            sys.exit(1)
    else:
        user_data = collect_interactive_data()

    # Build the AI prompt
    try:
        prompt = build_prompt(user_data)
    except Exception as e:
        print("ERROR: Failed to build prompt:", e)
        sys.exit(1)

    # Call the AI model
    try:
        raw_output = generate_recommendation(prompt)
    except Exception as e:
        print("ERROR: Model/API call failed:", e)
        sys.exit(1)

    # Parse the JSON output
    try:
        checklist = json.loads(raw_output)
    except json.JSONDecodeError as e:
        print("ERROR: Failed to parse JSON:", e)
        print("Raw output:\n", raw_output)
        sys.exit(1)

    # Fill missing fields and print final checklist
    for section, tasks in checklist.items():
        if isinstance(tasks, list):
            checklist[section] = [fill_missing_fields(t) for t in tasks]
    print(json.dumps(checklist, indent=4))

if __name__ == '__main__':
    main()
