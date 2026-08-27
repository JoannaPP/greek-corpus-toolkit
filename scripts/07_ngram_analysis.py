import json
from corpus_toolkit.preprocessor import clean_text
from corpus_toolkit.collocations import extract_tokens
from corpus_toolkit.ngram_analysis import analyze_ngrams

# Load stop words
with open("data/stopwords_el.json", "r", encoding="utf-8") as f:
    stopwords = set(json.load(f)["stopwords"])

# Load dataset
print("Loading corpus dataset...")
with open("data/corpus.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

full_text = " ".join([doc["text"] for doc in articles if "text" in doc])
cleaned_text = clean_text(full_text)

# Tokenize into clean lemmas
print("Extracting lemmas for N-gram processing...")
tokens = extract_tokens(cleaned_text, stopwords)

# Run N-Gram Analysis
top_unigrams, top_bigrams, top_trigrams = analyze_ngrams(tokens, top_n=10)

def print_ngram_table(title, items):
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)
    print(f"{'N-Gram':<35} | {'Frequency':<10}")
    print("-" * 50)
    for ngram, freq in items:
        print(f"{ngram:<35} | {freq:<10}")
    print("="*50)

print_ngram_table("TOP 10 UNIGRAMS (1-grams)", top_unigrams)
print_ngram_table("TOP 10 BIGRAMS (2-grams)", top_bigrams)
print_ngram_table("TOP 10 TRIGRAMS (3-grams)", top_trigrams)