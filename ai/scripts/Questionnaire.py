# questionnaire.py

questionnaire = {
    "basic_info": [
        "What is your full name?", 
        "What is your age?",
        "What is your nationality?",
        "What type of visa do you have (Work, Student, Residency, Tourist, etc.)?",
        "Are you moving alone or with family? (If family, specify number of members)",
        "What is your estimated migration budget? (Low, Medium, High)",
        "Do you have pets? (Yes/No)"
    ],

    "pre_departure": [
        "What is your destination country and city?",
        "What is your preferred housing type? (Apartment, House, Shared Housing)",
        "Do you already have a job lined up? (Yes/No)",
        "If not, what industry are you looking to work in?",
        "What is your expected arrival date?",
        "What are your primary concerns about relocating? (Legal paperwork, housing, job search, financial planning, cultural adaptation, etc.)"
    ],

    "departure_travel": [
        "Have you booked your flight or transportation to your new country? (Yes/No)",
        "Do you need assistance with packing and moving services? (Yes/No)",
        "Do you require pet relocation services? (Yes/No)",
        "Are you carrying restricted or special items that require customs clearance? (Yes/No)",
        "Do you need assistance with currency exchange before travel? (Yes/No)",
        "Do you need information on travel insurance? (Yes/No)",
        "Would you like reminders for important pre-departure tasks? (Yes/No)"
    ],

    "departure_housing": [
        "Do you want to rent or buy?",
        "What is your budget range for housing? (Low, Medium, High)",
        "Do you need a furnished place? (Yes/No)",
        "How important is proximity to public transport? (Very Important, Somewhat Important, Not Important)",
        "Do you need pet-friendly housing? (Yes/No)"
    ],

    "departure_job_finance": [
        "Do you need assistance finding a job? (Yes/No)",
        "If yes, what is your preferred industry/job role?",
        "Do you need help opening a bank account in your new country? (Yes/No)",
        "Are you looking for financial planning advice? (Yes/No)"
    ],

    "departure_healthcare": [
        "Do you need help finding health insurance? (Yes/No)",
        "Do you have any existing medical conditions that require specific healthcare access? (Yes/No)",
        "If yes, specify the condition(s) for better recommendations"
    ],

    "departure_legal": [
        "Do you need assistance with visa processing? (Yes/No)",
        "Do you need to transfer any licenses or certifications? (Yes/No)",
        "Do you need legal assistance for residency or work permits? (Yes/No)"
    ],

    "post_arrival": [
        "Do you need help setting up utilities (electricity, internet, water, etc.)? (Yes/No)",
        "Are you looking for language-learning programs? (Yes/No)",
        "Do you need help enrolling in schools/universities for yourself or your children? (Yes/No)",
        "Do you need help setting up a rental agreement? (Yes/No)",
        "Are you interested in understanding local labor laws and employee rights? (Yes/No)",
        "Do you need assistance with citizenship or long-term residency options? (Yes/No)",
        "Do you need help finding childcare or daycare services? (Yes/No)",
        "Do you need help setting up a local bank account? (Yes/No)",
        "Are you interested in getting a local credit card or loan options? (Yes/No)",
        "Do you need guidance on tax regulations in your new country? (Yes/No)"
    ]
}

def collect_responses():
    print("\nWelcome to Smooth Migration — Let's get to know your move 👇\n")
    responses = {}

    for section, questions in questionnaire.items():
        print(f"\n--- {section.replace('_', ' ').title()} ---")
        responses[section] = []

        for question in questions:
            answer = input(f"{question}\n> ").strip()
            responses[section].append({
                "question": question,
                "answer": answer
            })

    return responses

if __name__ == "__main__":
    user_data = collect_responses()

    # Print summary (optional)
    import json
    print("\n✅ All responses collected:\n")
    print(json.dumps(user_data, indent=4))
