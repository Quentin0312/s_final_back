from spacy.language import Language

# fmt: off
# TODO: add more ! (NOT "'" => mot composé géré par spacy !)
special_chars = [":","@","^","!","?","=","*","/","\"", ",", ";", "[", "]", "€", "(", ")","0","1","2","3","4","5","6","7","8","9","_",".",">","<","-"]
# * "'" => delete only " ' " via removing single letters !
not_a_word_letters = ["'","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","w","v","x","y","z"]
# fmt: on


def clean_text(text: str) -> str:
    # Lower case all letters
    text = text.lower()

    # Remove special chars
    for char in special_chars:
        text = text.replace(char, " ")  # OR replace(char, "") => dont cut word !?

    # Remove single letters
    for letter in not_a_word_letters:
        text = text.replace(" " + letter + " ", "   ")

    # Removes spaces
    while text.find("  ") != -1:
        text = text.replace("  ", " ")

    return text


def remove_out_of_vocabulary_words(text: str, nlp: Language) -> str:
    """
    Remove words that are out of vocabulary of the arg nlp Language

    Carrefull: Even if arg nlp language is `fr_core_news_lg`, non french
        tokens can be in the vocabulary !
    """
    new_token_list = []
    for token in text.split(" "):
        if not (nlp.vocab[token].is_oov):
            new_token_list.append(token)

    text = " ".join(new_token_list)

    return text


def lemmatize(text: str, nlp: Language) -> str:
    """
    Lemmatize is replacing a word with it's root word.

    Exemple: portables => portable
    """
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


def pipeline_from_raw_text_to_vectors(
    raw_text: str, nlp: Language, vocabulary: list[str]
) -> list[int]:
    """
    To use after vocabulary is done (for test and inference)
    """
    cleaned_text = full_cleaning(raw_text, nlp)

    return get_bags_of_words_vector(cleaned_text, vocabulary)


def full_cleaning(raw_text: str, nlp: Language) -> str:
    cleaned_text_content = clean_text(raw_text)
    filtered_text_content = remove_out_of_vocabulary_words(cleaned_text_content, nlp)
    return lemmatize(filtered_text_content, nlp)
