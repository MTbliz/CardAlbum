import re


def remove_special_characters(text: str) -> str:
    clean_text: str = re.sub(r"[^a-zA-Z0-9 ]", "", text)
    return clean_text


def concatenate_words_in_string(text: str):
    words: list[str] = text.split(" ")
    return '+'.join(words)


def capitalize_string(text: str) -> str:
    articles: list[str] = ['a', 'an', 'the']
    prepositions: list[str] = ['in', 'on', 'at', 'by', 'for', 'from', 'of', 'with', 'to']
    conjunctions: list[str] = ['and', 'but', 'or', 'so', 'yet']

    words: list[str] = text.split(" ")
    capitalized_words: list[str] = [word.title() if word not in articles + prepositions + conjunctions else word for
                                    word in words]

    # Join the words back together into a string
    return ' '.join(capitalized_words)
