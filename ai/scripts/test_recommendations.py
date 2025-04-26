import requests


url = "http://127.0.0.1:5000/recommendations"


sample_data = {
    "full_name": "Alex Johnson",
    "age": 29,
    "nationality": "Canadian",
    "visa_type": "Work",
    "moving_with_family": "Yes, 2 family members",
    "budget": "Medium",
    "has_pets": "No",
    "destination_country_city": "Germany, Berlin",
    "preferred_housing": "Apartment",
    "has_job": "No",
    "job_industry": "Software Engineering",
    "arrival_date": "2025-08-01",
    "concerns": "Job search, cultural adaptation",
    "booked_flight": "Yes",
    "packing_help": "Yes",
    "pet_relocation": "No",
    "customs_clearance": "No",
    "currency_exchange": "Yes",
    "travel_insurance": "Yes",
    "predeparture_reminders": "Yes",
    "rent_or_buy": "Rent",
    "housing_budget": "Medium",
    "furnished": "Yes",
    "public_transport_importance": "Very Important",
    "pet_friendly_housing": "No",
    "job_assistance": "Yes",
    "job_role": "Backend Developer",
    "bank_account_help": "Yes",
    "financial_planning": "Yes",
    "health_insurance": "Yes",
    "medical_conditions": "No",
    "visa_processing": "No",
    "transfer_certifications": "Yes",
    "legal_assistance": "Yes",
    "utilities_setup": "Yes",
    "language_programs": "Yes",
    "school_enrollment": "No",
    "rental_agreement_help": "Yes",
    "labor_laws_info": "Yes",
    "citizenship_help": "No",
    "childcare": "No",
    "local_bank_setup": "Yes",
    "credit_loan_info": "Yes",
    "tax_guidance": "Yes"
}


response = requests.post(url, json=sample_data)


print(" Mock Test Response:")
print(response.status_code)
print(response.json())
