

from scripts.questionnaire import get_all_questions

def build_prompt(user_data: dict) -> str:
    """
    Construct a GPT prompt from the full questionnaire and the user's answers.
    :param user_data: dict mapping question string -> answer string
    :return: formatted prompt
    """
    questions = get_all_questions()

    
    prompt = (
        "You are a smart and helpful migration assistant AI.\n"
        "Based on the user's answers to the following relocation questionnaire, "
        "provide a personalized, step-by-step migration plan:\n\n"
    )

    
    for q in questions:
        answer = user_data.get(q, "Not answered")
        prompt += f"Q: {q}\nA: {answer}\n\n"

    
    prompt += "Please generate detailed migration recommendations tailored to the user's responses above."

    return prompt

