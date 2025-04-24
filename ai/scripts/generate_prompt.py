def build_prompt(user_data: dict) -> str:
    """
    Constructs a natural-language prompt from the structured user responses.

    Args:
        user_data (dict): Dictionary with categorized user responses.

    Returns:
        str: A prompt string summarizing the user's migration context.
    """
    prompt_parts = []
    
    # Iterate over each category in the user data
    for section, qa_list in user_data.items():
        # Use plain headers (e.g., "Pre-Departure", "Basic Info")
        section_header = section.replace('_', ' ').title()
        section_details = f"{section_header}:\n"
        
        for qa in qa_list:
            question = qa.get("question", "").strip()
            answer = qa.get("answer", "").strip()
            if question and answer:
                section_details += f"  - Question: {question} | Answer: {answer}\n"
        
        # Only append if section has content
        if section_details.strip() != f"{section_header}:":
            prompt_parts.append(section_details.strip())
    
    # Combine all parts into a formatted details block
    details = "\n".join(prompt_parts).strip()
    
    # Build the final natural-language prompt for LLM
    final_prompt = (
        "Generate a detailed migration checklist based on the following user information. "
        "The checklist should be structured as valid JSON with exactly three sections: "
        "'Pre-Departure', 'Departure', and 'Post-Departure'. Each section must contain a list of task objects "
        "with the keys 'task', 'phase', and 'api_trigger'.\n\n"
        "User Details:\n"
        f"{details}"
    )
    
    return final_prompt