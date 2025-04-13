import openai
from dotenv import load_dotenv
import os
from scripts.generate_prompt import build_questionnaire_prompt


load_dotenv()


openai.api_key = os.getenv(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
)

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
