import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the API key for the OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")

client = OpenAI(api_key=api_key)

def generate_recommendation(prompt: str) -> str:
    """
    Generates a structured migration checklist using the OpenAI Chat API.
    The model must return a valid JSON object with the keys 'Pre-Departure', 'Departure', and 'Post-Departure'.
    Each key maps to a list of task dictionaries with 'task', 'phase', and 'api_trigger'.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a migration planning assistant. Given a user’s relocation context, "
                        "generate a detailed migration checklist structured as valid JSON only. "
                        "Your response must contain exactly three top-level keys: 'Pre-Departure', 'Departure', and 'Post-Departure'. "
                        "Each should contain a list of task objects with the fields: \n"
                        "- task (string): A short description of the task\n"
                        "- phase (string): Either 'Pre-Departure', 'Departure', or 'Post-Departure'\n"
                        "- api_trigger (string|null): An identifier for API triggers (e.g., 'car_rental', 'job_search') or null if not applicable.\n\n"
                        "Respond ONLY with JSON. No explanations or markdown."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.6
        )

        recommendation = response.choices[0].message.content.strip()

        # Remove markdown code block wrappers if present
        if recommendation.startswith("```"):
            recommendation = re.sub(r"^```(?:json)?", "", recommendation)
            recommendation = recommendation.rstrip("```").strip()

        return recommendation

    except Exception as e:
        print("Error generating recommendation:", e)
        return ""

if __name__ == "__main__":
    # Example usage
    sample_prompt = (
        "Generate a migration checklist for a user relocating from the USA to Germany for a tech job. "
        "They have one child, are renting, and plan to leave in two months. "
        "Structure the checklist using only valid JSON with task, phase, and api_trigger fields."
    )

    recommendation = generate_recommendation(sample_prompt)

    print("🔹 Raw JSON Output:")
    print(recommendation)

    try:
        parsed = json.loads(recommendation)
        print("\n✅ Parsed JSON Output:")
        print(json.dumps(parsed, indent=4))
    except json.JSONDecodeError as err:
        print("\n❌ Invalid JSON Output:")
        print("JSONDecodeError:", err)
