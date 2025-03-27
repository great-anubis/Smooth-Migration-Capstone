import os
from openai import OpenAI  # Import the new client interface
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Instantiate the OpenAI client with the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def generate_recommendation(prompt: str) -> str:
    """
    Generates a recommendation using the new OpenAI Chat API interface.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        # Access the message content from the response object
        recommendation = response.choices[0].message.content.strip()
        return recommendation
    except Exception as e:
        print("Error generating recommendation:", e)
        return ""

if __name__ == "__main__":
    # Example prompt for testing
    sample_prompt = (
        "Generate a migration checklist for a user moving from the USA to Canada "
        "with a family of 3. Include pre-departure, departure, and post-departure tasks."
    )
    recommendation = generate_recommendation(sample_prompt)
    print("Generated Recommendation:")
    print(recommendation)
