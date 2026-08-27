import json
import re
import spacy

# Load spaCy Greek model
nlp = spacy.load("el_core_news_sm")

# Load your custom stop words file
with open("data/stopwords_el.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    stopwords = set(data["stopwords"])


def clean_text(text):
    """Removes duplicate whitespace and normalizes text."""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def split_sentences(text):
    """Splits raw text into a list of sentences using spaCy."""
    doc = nlp(text)
    return [sent.text.strip() for sent in doc.sents]


def tokenize(text, remove_stopwords=True, greek_only=True):
    """Tokenizes text, stripping out punctuation and custom stop words."""
    doc = nlp(text)
    tokens = []

    for token in doc:
        word_lower = token.text.lower()

        # Skip punctuation and spaces
        if token.is_punct or token.is_space:
            continue
            
        # Skip stop words if enabled
        if remove_stopwords and word_lower in stopwords:
            continue

        # Filter non-Greek tokens (if enabled)
        if greek_only and not re.search(r"[α-ωΑ-Ωά-ώ]", word_lower):
            continue

        tokens.append(token.text)

    return tokens