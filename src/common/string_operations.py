import re


def remove_special_characters(text: str) -> str:
    clean_text = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    return clean_text


def concatenate_words_in_string(text: str):
    words = text.split(" ")
    return '+'.join(words)


def capitalize_string(text: str):
    articles = ['a', 'an', 'the']
    prepositions = ['in', 'on', 'at', 'by', 'for', 'from', 'of', 'with', 'to']
    conjunctions = ['and', 'but', 'or', 'so', 'yet']

    words = text.split(" ")
    capitalized_words = [word.title() if word not in articles + prepositions + conjunctions else word for word in
                         words]

    # Join the words back together into a string
    return ' '.join(capitalized_words)
