import openai
from scripts.generate_prompt import build_questionnaire_prompt


openai.api_key = "your-openai-api-key"  

def get_recommendation_from_questionnaire():
    prompt = build_questionnaire_prompt()

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a migration assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error calling AI engine: {e}"
