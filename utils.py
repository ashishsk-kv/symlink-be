import string

def map_keys(list_of_keys):
    map = {}
    for keys in list_of_keys:
        if keys["identifier"] not in map:
            map[keys["identifier"]] = keys["entity"]
    return map

def reverse_map(text, map):
    words = text.split(' ')
    for index in range(len(words)):
        search_key = words[index].translate(str.maketrans('', '', string.punctuation))
        # print(search_key)
        if search_key in map:
            words[index] = words[index].replace(search_key, map[search_key])
    return ' '.join(words)

def clean_white_space(text):
    if not text:
        return ''
    return " ".join(text.split())


def clean_entity(text):
    """
    to clean ner predictions from hugging face pipeline"
    """
    if not text:
        return
    text = text.replace('#', '')
    return " ".join(text.split())