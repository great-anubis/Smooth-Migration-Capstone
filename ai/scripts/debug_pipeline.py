import json
import sys
import os

# Add src to the import path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'app'))

from generate_prompt import build_prompt_from_user_data
from ai_engine import get_checklist_from_ai

def main():
    if len(sys.argv) != 2:
        print("Usage: python debug_pipeline.py <input_json_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    
    with open(input_file, 'r') as f:
        user_data = json.load(f)

    print("🧠 Building prompt...")
    prompt = build_prompt_from_user_data(user_data)
    print("\n🔧 Prompt sent to AI:\n", prompt)

    print("\n📬 Getting AI-generated checklist...")
    checklist = get_checklist_from_ai(prompt)

    print("\n✅ Final Checklist Output:\n")
    print(json.dumps(checklist, indent=2))

if __name__ == "__main__":
    main()
