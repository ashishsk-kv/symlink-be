import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # PostgreSQL database URL
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Use a secure secret key for sessions
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")

# llm_model_path = "mistral:7b-instruct-v0.3-q8_0"
llm_model_path = "llama3.1:8b-instruct-q8_0"
# llm_model_path = "llama3.2:3b-instruct-q8_0"
faker_providers = {
    'ORG': 'fake.company()',            # Organization name
    'STREET': 'fake.street_address()',   # Street address
    'CITY': 'fake.city()',               # City name
#     'LOC': 'fake.location_on_land()',    # Location (latitude, longitude)
    'PER': 'fake.name()',
    'GIVENNAME': 'fake.first_name()',    # First (given) name
    'SURNAME': 'fake.last_name()',       # Surname (last name)
    'ZIPCODE': 'fake.zipcode()',         # ZIP code
    'TELEPHONENUM': 'fake.phone_number()',# Telephone number
    'EMAIL': 'fake.email()',             # Email address
    'DRIVERLICENSENUM': 'fake.license_plate()', # Driver's license number (as license plate)
    'ACCOUNTNUM': 'fake.iban()',         # Account number (can be IBAN for generic purposes)
}
perssonal_info_ner = "iiiorg/piiranha-v1-detect-personal-information"
org_loc_ner = 'dslim/bert-base-NER'
ner_labels = [
          'LOC', 'ORG', 'PER',
          'ACCOUNTNUM', 
          'CITY', 
          'CREDITCARDNUMBER', 'DATEOFBIRTH', 'DRIVERLICENSENUM', 'EMAIL', 'GIVENNAME', 'IDCARDNUM', 'PASSWORD', 'SOCIALNUM', 'STREET', 'SURNAME', 'TAXNUM', 'TELEPHONENUM', 'USERNAME', 'ZIPCODE']

prompt_3 = """Identify and replace all entities in the following text that are either persons, institutions, or places with a unique identifier throughout the entire text. This includes replacing both the full entity name and any partial occurrences of the name (e.g., replacing "Micky Mouse" and "Micky" with the same identifier). The intent of the user must not be altered during this process. Do not add any additional notes to the message. Please ensure to mask every possible sensitive information that could lead to data leak. Steps: * Identify all entities in the text that are classified as 'Location', 'Organization', 'persons', 'account number', 'City', 'CREDITCARDNUMBER', 'DATEOFBIRTH', 'DRIVERLICENSENUM', 'EMAIL', 'IDCARDNUM', 'PASSWORD', 'SOCIALNUM', 'STREET', 'TAXNUM', 'TELEPHONENUM', 'USERNAME', 'ZIPCODE', 'PHONE_NUMBER', 'EMAIL_ADDRESS', and other information. * Assign a unique identifier to each entity while ensuring that the context and intent of the user are preserved. * Replace every occurrence of the full name and any partial name with the corresponding identifier in the text, making sure that the meaning remains clear. * Print the processed text with all entities replaced by their respective identifiers. Do NOT print the original text but only the processed version. * Provide a JSON-formatted list of all replaced entities as pairs, where each pair consists of the entity name and its corresponding identifier. Example, follow the format strictly: Original text: "Micky Mouse is a character created by Walt Disney. You can contact him at micky@example.com or (555) 123-4567 to discuss the project." Output: { "processed_text": "ENTITY1 is a character created by ENTITY2. You can contact him at ENTITY3 or ENTITY4 to discuss the project.", "entities": [ {"entity": "Micky Mouse", "identifier": "ENTITY1"}, {"entity": "Micky", "identifier": "ENTITY1"}, {"entity": "Walt Disney", "identifier": "ENTITY2"}, {"entity": "Walt", "identifier": "ENTITY2"}, {"entity": "micky@example.com", "identifier": "ENTITY3"}, {"entity": "(555) 123-4567", "identifier": "ENTITY4"} ] } Text to be formatted: """
prompt = """Identify and replace all entities in the following text that are either
                persons, institutions, or places with a unique identifier throughout the
                entire text. This includes replacing both the full entity name and any
                partial occurrences of the name (e.g., replacing "Micky Mouse" and "Micky"
                with the same identifier). The intent of the user must not be altered during this process.
                Do not add any additional notes to the message.
                Steps:
                    * Identify all entities in the text that are classified as 'Location', 'Organization', 'persons', 'account number', 'City', 'CREDITCARDNUMBER', 'DATEOFBIRTH', 'DRIVERLICENSENUM', 'EMAIL',  'IDCARDNUM', 'PASSWORD', 'SOCIALNUM', 'STREET',  'TAXNUM', 'TELEPHONENUM', 'USERNAME', 'ZIPCODE', 'PHONE_NUMBER', 'EMAIL_ADDRESS', and other sensitive information.
                    * Mask sensitive information, such as account numbers and social security numbers.
                    * Assign a unique identifier to each entity using the format Entity_A, Entity_B, Entity_C, etc., while ensuring that the context and intent of the user are preserved.
                    * Replace every occurrence of the full name and any partial name with the corresponding identifier in the text, making sure that the meaning remains clear.
                    * Print the processed text with all entities replaced by their respective identifiers. Do NOT print the original text but only the processed version.
                    * Provide a JSON-formatted list of all replaced entities as pairs, where each pair consists of the entity name and its corresponding identifier.
                Example, follow the format strictly:
                    Original text: "Micky Mouse is a character created by Walt Disney. You can contact him at micky@example.com or (555) 123-4567 to discuss the project. His account number is 987654321."
                    Output: {
                        "processed_text": "Entity_A is a character created by Entity_B. You can contact him at Entity_C or Entity_D to discuss the project. His account number is [MASKED].",
                        "entities": [
                            {"entity": "Micky Mouse", "identifier": "Entity_A"},
                            {"entity": "Micky", "identifier": "Entity_A"},
                            {"entity": "Walt Disney", "identifier": "Entity_B"},
                            {"entity": "Walt", "identifier": "Entity_B"},
                            {"entity": "micky@example.com", "identifier": "Entity_C"},
                            {"entity": "(555) 123-4567", "identifier": "Entity_D"},
                            {"entity": "987654321", "identifier": "[MASKED]"}
                        ]
                    }
                Text to be formatted: """
prompt_2 = """Identify and replace all entities in the following text that are either 
        persons, institutions, or places with a unique identifier throughout the 
        entire text. This includes replacing both the full entity name and any 
        partial occurrences of the name (e.g., replacing "Micky Mouse" and "Micky" 
        with the same identifier). Do not add any additional notes to the message.

        Steps:

            * Identify all entities in the text that are classified as 'Location', 'Organization', 'persons', 'account number', 'City', 'CREDITCARDNUMBER', 'DATEOFBIRTH', 'DRIVERLICENSENUM', 'EMAIL',  'IDCARDNUM', 'PASSWORD', 'SOCIALNUM', 'STREET',  'TAXNUM', 'TELEPHONENUM', 'USERNAME', 'ZIPCODE' and other informations.
            * Assign a unique identifier to each entity.
            * Replace every occurrence of the full name and any partial name with the corresponding identifier in the text.
            * Print the processed text with all entities replaced by their respective identifiers. Do NOT print the original text but only the processed version.
            * Provide a JSON-formatted list of all replaced entities as pairs, where each pair consists of the entity name and its corresponding identifier.

        Example, follow the format strictly:

            Original text: "Micky Mouse is a character created by Walt Disney."
            Output: {
                "processed_text": "ENTITY1 is a character created by ENTITY2.",
                "entities": [
                    {"entity": "Micky Mouse", "identifier": "ENTITY1"},
                    {"entity": "Micky", "identifier": "ENTITY1"},
                    {"entity": "Walt Disney", "identifier": "ENTITY2"},
                    {"entity": "Walt", "identifier": "ENTITY2"}
                ]
            }
        
        Text to be formatted: """