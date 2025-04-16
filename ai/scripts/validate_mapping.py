import json
import os

def load_mapping(mapping_path):
    with open(mapping_path, "r") as f:
        data = json.load(f)
    return data

if __name__ == "__main__":
    mapping_file = os.path.join(os.path.dirname(__file__), "checklist_mapping.json")
    try:
        mapping = load_mapping(mapping_file)
        print("Checklist Mapping Loaded Successfully:")
        print(json.dumps(mapping, indent=4))
    except Exception as e:
        print("Error loading mapping file:", e)
