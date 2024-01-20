from spacy.language import Language

# fmt: off
special_chars = ["/","\"", ",", ";", "[", "]", "€", "(", ")","0","1","2","3","4","5","6","7","8","9","_",".",">","<","-"]  # TODO: add more ! (NOT "'" => mot composé géré par spacy !)
not_a_word_letters = ["b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","w","v","x","y","z"]
# fmt: on


def clean_text(text: str) -> str:
    # Lower case all letters
    text = text.lower()

    # Remove special chars
    for char in special_chars:
        text = text.replace(char, " ")

    # Remove single letters
    for letter in not_a_word_letters:
        text = text.replace(" " + letter + " ", "   ")

    # Removes spaces
    while text.find("  ") != -1:
        text = text.replace("  ", " ")

    return text


def remove_out_of_vocabulary_words(text: str, nlp: Language) -> str:
    new_token_list = []
    for token in text.split(" "):
        if not (nlp.vocab[token].is_oov):
            new_token_list.append(token)

    text = " ".join(new_token_list)

    return text


def lemmatize(text: str, nlp: Language) -> str:
    tokens = nlp(text)

    lemmatized_tokens = [token.lemma_ for token in tokens]
    lemmatized_text = " ".join(lemmatized_tokens)

    return lemmatized_text


def get_bags_of_words_vector(text: str, vocabulary: list[str]) -> list[int]:
    """
    BOW Feature extraction
    """
    tokens = text.split(" ")

    vector = []
    for word in vocabulary:
        vector.append(tokens.count(word))

    return vector
