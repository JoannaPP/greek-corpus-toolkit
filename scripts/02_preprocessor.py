import json
from corpus_toolkit.preprocessor import clean_text, split_sentences, tokenize

# 1. Load raw corpus from JSON file
print("Loading scraped corpus dataset...")
with open("data/corpus.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

print(f"Successfully loaded {len(articles)} articles.")

# 2. Combine all article texts into one full corpus string
full_corpus_text = " ".join([doc["text"] for doc in articles])

# 3. Clean raw text
cleaned_text = clean_text(full_corpus_text)

# 4. Process tokens with custom stop words and punctuation removed
print("\nTokenizing corpus with custom Modern Greek stopwords removed...")
tokens = tokenize(cleaned_text, remove_stopwords=True)

# 5. Display core pre-processing results
print("\n" + "="*40)
print("       PREPROCESSING RESULTS")
print("="*40)
print(f"Total Articles Processed : {len(articles)}")
print(f"Total Filtered Tokens    : {len(tokens)}")
print(f"Sample Tokens (First 20) :")
print(tokens[:20])
print("="*40)