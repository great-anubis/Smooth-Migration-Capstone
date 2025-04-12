from scripts.Questionnaire import questionnaire

def build_questionnaire_prompt():
    prompt = "You are an AI migration assistant.\n"
    prompt += "Below is the adaptive migration questionnaire structure used to gather user preferences and constraints:\n"

    for section, questions in questionnaire.items():
        section_title = section.replace('_', ' ').title()
        prompt += f"\n[{section_title} Questions]\n"
        for q in questions:
            prompt += f"- {q}\n"

    prompt += "\nUse this structure to guide your understanding of what the user may need when relocating internationally. Do not answer yet — wait for user answers to generate personalized recommendations."
    return prompt
