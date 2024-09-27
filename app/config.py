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
# llm_model_path = "llama3.1:8b-instruct-q8_0"
llm_model_path = "ghost_ai:latest"
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
# ner_labels = [
#           'LOC', 'ORG', 'PER',
#           'ACCOUNTNUM', 
#           'CITY', 
#           'CREDITCARDNUMBER', 'DATEOFBIRTH', 'DRIVERLICENSENUM', 'EMAIL', 'GIVENNAME', 'IDCARDNUM', 'PASSWORD', 'SOCIALNUM', 'STREET', 'SURNAME', 'TAXNUM', 'TELEPHONENUM', 'USERNAME', 'ZIPCODE']
# ner_labels = ['ORG', 'PER', 'ACCOUNTNUM', 'CREDITCARDNUMBER',  'DRIVERLICENSENUM', 'EMAIL',  'IDCARDNUM',  'SOCIALNUM', 'STREET', 'TELEPHONENUM']
meaningful_names = {
    'ORG': 'Organization',
    'PER': 'Person',
    'ACCOUNTNUM': 'Account Number',
    'CREDITCARDNUMBER': 'Credit Card Number',
    'DRIVERLICENSENUM': 'Driver License Number',
    'EMAIL': 'Email Address',
    'IDCARDNUM': 'ID Card Number',
    'SOCIALNUM': 'Social Security Number',
    'STREET': 'Street Address',
    'TELEPHONENUM': 'Telephone Number'
}
ner_labels = list(meaningful_names.keys())
llm_labels = ", ".join(list(meaningful_names.values()))

prompt_pencil = """You need to perfom Named entity recognition to identify the PII information without considering the users prompt intent, no other details needed.
Steps:
* Identify all entities in the text that are sensitive information and add a very specific short description as shown in the example below. Also, if multiple instances of same category occurs use synonyms.
Example, for the content: generate an ad for Nike Air Jordan, Output will be a python dictionary as follows {"Nike": "shoe company", "Air Jordan": "Basket Ball shoes"},
Strictly follow the output signature, no other details needed, Text to be identified:
"""

prompt_main = """You need to perfom Named entity recognition to identify the PII information without considering the users prompt intent, no other details needed.
Steps:
* Identify all entities in the text that are classified as Organization, Person, Account Number, Credit Card Number, Driver License Number, Email Address, ID Card Number, Social Security Number, Street Address and Telephone Number
Example, for the content: Micky Mouse is a character created by Walt Disney. You can contact him at micky@example.com or (555) 123-4567 to discuss the project.  Output will be a python list as follows ['Micky Mouse', 'Walt Disney', 'micky@example.com', '(555) 123-4567', '987654321'],
Strictly follow the output signature, no other details needed, Text to be identified:
"""

demo_type = "PII-IDENTIFICATION"
# demo_type = "PENCIL"
prompt = prompt_pencil if demo_type == "PENCIL" else prompt_main