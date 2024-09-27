from .custom_ner import CustomTransformerNER
from faker import Faker
from app.config import org_loc_ner, perssonal_info_ner, ner_labels
from app.utils import clean_white_space

fake = Faker('en')
ner_personal_info = CustomTransformerNER(model_path=perssonal_info_ner, labels=ner_labels)
ner_org = CustomTransformerNER(model_path=org_loc_ner, labels=ner_labels)

def get_prediction(user_msg):
    """
    return the prediction for NER on user msg
    """
    cleaned_text = clean_white_space(user_msg)
    results = ner_org.get_results(cleaned_text)
    results.update(ner_personal_info.get_results(cleaned_text))
    #mapped_entities = {key : eval(faker_providers.get(value)) for key, value in results.items() if faker_providers.get(value)}
    
    mapped_entities = [{"entity": key, "identifier": f"ENTITY{idx+1}"} for idx, key in enumerate(results)]
    for entity_details in mapped_entities:
        real_entity, masked_entity = entity_details.values()
        cleaned_text = cleaned_text.replace(real_entity, masked_entity)
    return cleaned_text, mapped_entities

