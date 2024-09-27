import ollama
from config import llm_model_path, prompt

def query_model_using_ollama(prompt):
    try:
        # Send the request to the Ollama API
        print("loading llm model_path", llm_model_path)
        model_response = ollama.generate(llm_model_path, prompt)
        return model_response['response']
    except Exception as e:
        raise Exception(f"Failed to query model: Exception: {e}")
    

def query(user_prompt):
    try:
        final_prompt = prompt + user_prompt
        result = query_model_using_ollama(final_prompt)
        return result
    except Exception as e:
        print(f"Excetption: {e}")