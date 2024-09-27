from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from app.utils import clean_entity


class CustomTransformerNER():
    def __init__(self, **kwargs):
        # Initialize the Hugging Face pipeline for NER
        self.tokenizer = AutoTokenizer.from_pretrained(kwargs.get("model_path"))
        self.model = AutoModelForTokenClassification.from_pretrained(kwargs.get("model_path"))
        self.ner_pipeline = pipeline("ner", model=self.model, tokenizer=self.tokenizer, aggregation_strategy="simple")
        self.supported_entities = kwargs.get("labels")

    def get_results(self, text, confidence=0.90):
        ner_results = self.ner_pipeline(text)
        ner_results = [dict(res, idx=idx) for idx, res in enumerate(ner_results)]
        found = []
        final_results = {}
        final_results_with_conf = []
        for idx, entity in enumerate(ner_results):
            class_ = entity['entity_group']
            if class_ not in self.supported_entities:
                continue
            end = entity['end']
            first_entity_confidence = entity['score']
            if first_entity_confidence < confidence:
                continue
            start_body = entity['word']
            current_idx = entity['idx']
            entity.update()
            if current_idx in found:
                continue
            found.append(current_idx)
            for next_entity in ner_results[current_idx+1:]:
                next_idx = next_entity['idx']
                if next_idx in found:
                    continue
                start_end_diff = next_entity['start'] - end
                conditions = [
                    next_entity['entity_group'] != class_,
                    start_end_diff > 1]
                if any(conditions):
                    break
                if start_end_diff == 1:
                    start_body = start_body + " " + next_entity['word']
                else:
                    start_body += next_entity['word']
                found.append(next_idx)
                end = next_entity['end']
            final_results[clean_entity(start_body)] = class_
#             final_results_with_conf.append(
#                 {"class_name": class_, 
#                  "entity": clean_entity(start_body), 
#                  "first_entity_confidence": first_entity_confidence})
        return final_results


