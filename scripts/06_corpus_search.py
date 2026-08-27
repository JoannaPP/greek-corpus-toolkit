import json
import spacy
from corpus_toolkit.corpus_search import search_keyword, search_regex, search_by_pos

# Load spacy model and corpus dataset
print("Loading spaCy model...")
nlp = spacy.load("el_core_news_sm")

print("Loading corpus dataset...")
with open("data/corpus.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Combine corpus into a single text for searching
full_text = " ".join([doc["text"] for doc in articles if "text" in doc])

print("Processing text with spaCy (this may take a moment)...")
doc = nlp(full_text)

print("\n" + "="*80)
print(" CORPUS SEARCH ENGINE")
print("="*80)

# 1. KEYWORD SEARCH
user_word = input("\n[1] Enter a word to search (e.g., ελλάδα, κυβέρνηση) or press ENTER to skip: ").strip()
if user_word:
    total, samples = search_keyword(doc, user_word)
    print("\n--- KEYWORD SEARCH RESULTS ---")
    print(f"Target word          : '{user_word}'")
    print(f"Total occurrences    : {total}")
    print(f"Sample matches       : {samples}")

# 2. REGEX SEARCH
user_regex = input("\n[2] Enter a regex pattern (e.g., ^\\d+.* for numbers) or press ENTER to skip: ").strip()
if user_regex:
    total, samples = search_regex(doc, user_regex)
    print("\n--- REGEX SEARCH RESULTS ---")
    print(f"Pattern              : '{user_regex}'")
    print(f"Total occurrences    : {total}")
    print(f"Sample matches       : {samples}")

# 3. POS TAG SEARCH
user_pos = input("\n[3] Enter a POS tag (e.g., NOUN, VERB, ADJ, PROPN) or press ENTER to skip: ").strip().upper()
if user_pos:
    total, samples = search_by_pos(doc, user_pos)
    print("\n--- POS TAG SEARCH RESULTS ---")
    print(f"POS Tag              : '{user_pos.upper()}'")
    print(f"Total occurrences    : {total}")
    print(f"Sample matches       : {samples}")

print("\n" + "="*80)