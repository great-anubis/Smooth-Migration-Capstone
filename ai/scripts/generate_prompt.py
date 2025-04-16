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
        # Convert section to a cleaner header (e.g., "Pre Departure")
        section_header = section.replace('_', ' ').title()
        section_details = f"**{section_header}:**\n"
        
        # Compile each question/answer pair into the prompt
        for qa in qa_list:
            question = qa.get("question", "").strip()
            answer = qa.get("answer", "").strip()
            # Append the Q/A in a natural-sounding sentence format
            section_details += f"- {question} {answer}. "
        
        prompt_parts.append(section_details)
    
    # Combine all parts into one complete string
    details = "\n".join(prompt_parts).strip()
    
    # Build the final natural-language prompt with context for the LLM
    final_prompt = (
        "Generate a detailed migration checklist based on the following user information. "
        "The checklist should be structured as valid JSON with exactly three sections: "
        "'Pre-Departure', 'Departure', and 'Post-Departure'. Each section must contain a list of task objects "
        "with the keys 'task', 'phase', and 'api_trigger'.\n\n"
        "User Details:\n"
        f"{details}"
    )
    
    return final_prompt

# --- For testing purposes ---
if __name__ == "__main__":
    # Example sample data similar to what the dynamic questionnaire would return.
    sample_user_data = {
        "basic_info": [
            {"question": "What is your full name?", "answer": "John Doe"},
            {"question": "What is your age?", "answer": "30"},
            {"question": "What is your nationality?", "answer": "Canadian"},
            {"question": "What type of visa do you have (Work, Student, Residency, Tourist, etc.)?",
             "answer": "Work"},
            {"question": "Are you moving alone or with family? (If family, specify number of members)",
             "answer": "With spouse"},
            {"question": "What is your estimated migration budget? (Low, Medium, High)",
             "answer": "Medium"},
            {"question": "Do you have pets? (Yes/No)", "answer": "Yes"}
        ],
        "pre_departure": [
            {"question": "What is your destination country and city?",
             "answer": "Germany, Berlin"},
            {"question": "What is your preferred housing type? (Apartment, House, Shared Housing)",
             "answer": "Apartment"},
            {"question": "Do you already have a job lined up? (Yes/No)", "answer": "No"},
            {"question": "If not, what industry are you looking to work in?",
             "answer": "Tech"},
            {"question": "What is your expected arrival date?", "answer": "2024-06-01"},
            {"question": "What are your primary concerns about relocating? (Legal paperwork, housing, job search, financial planning, cultural adaptation, etc.)",
             "answer": "job search and housing"}
        ],
        # You can include additional sections such as departure_travel, departure_housing, etc.
    }
    
    prompt = build_prompt(sample_user_data)
    print("Constructed Prompt:\n")
    print(prompt)
