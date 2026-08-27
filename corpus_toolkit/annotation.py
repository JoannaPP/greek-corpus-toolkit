import re
import spacy
from collections import Counter
from nltk import FreqDist

# Load spaCy Modern Greek model
nlp = spacy.load("el_core_news_sm")

def annotate_text(cleaned_text: str, custom_stopwords: set):
    """
    Annotates text with POS tags and Lemmas, filtering out noise and stopwords.
    Returns POS counts, filtered words, and filtered lemmas.
    """
    nlp.max_length = len(cleaned_text) + 1000
    doc = nlp(cleaned_text)

    pos_counts = Counter()
    words_filtered = []
    lemmas_filtered = []

    for token in doc:
        if token.is_punct or token.is_space:
            continue

        word = token.text.lower()
        lemma = token.lemma_.lower()
        pos = token.pos_

        pos_counts[pos] += 1
        is_greek = bool(re.search(r"[α-ωΑ-Ωά-ώ]", word))

        # Keeps only Greek words and removes custom Greek stopwords
        if is_greek and word not in custom_stopwords:
            words_filtered.append(word)
            lemmas_filtered.append(lemma)

    return pos_counts, words_filtered, lemmas_filtered

def get_frequencies(tokens: list):
    """Calculates frequency distribution of tokens using NLTK FreqDist."""
    return FreqDist(tokens)

def get_char_frequencies(text: str):
    """Calculates frequency distribution of characters (letters only)."""
    letters = [c for c in text.lower() if c.isalpha()]
    return FreqDist(letters)