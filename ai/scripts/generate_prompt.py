import json

def build_prompt(user_data: dict) -> str:

    prompt_parts = []

    for section, qa_list in user_data.items():
        section_header = section.replace('_', ' ').title()
        section_details = f"{section_header}:\n"

        for qa in qa_list:
            if isinstance(qa, dict):
                question = qa.get("question", "").strip()
                answer = qa.get("answer", "").strip()
                if question and answer:
                    section_details += f"  - Question: {question} | Answer: {answer}\n"
            elif isinstance(qa, str):
                section_details += f"  - Answer: {qa.strip()}\n"

        if section_details.strip() != f"{section_header}:":
            prompt_parts.append(section_details.strip())

    details = "\n".join(prompt_parts).strip()

    final_prompt = (
        "Generate a detailed migration checklist based on the following user information. "
        "The checklist should be structured as valid JSON with exactly three sections: "
        "'Pre-Departure', 'Departure', and 'Post-Departure'. Each section must contain a list of task objects "
        "with the keys 'task', 'phase', and 'api_trigger'.\n\n"
        "User Details:\n"
        f"{details}"
    )

    return final_prompt
