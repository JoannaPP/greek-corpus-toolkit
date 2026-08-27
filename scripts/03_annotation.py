import json
from corpus_toolkit.preprocessor import clean_text
from corpus_toolkit.annotation import annotate_text, get_frequencies, get_char_frequencies

# 1. Load custom stopwords
print("Loading stopwords...")
with open("data/stopwords_el.json", "r", encoding="utf-8") as f:
    stopwords = set(json.load(f)["stopwords"])

# 2. Load scraped corpus dataset
print("Loading scraped corpus dataset...")
with open("data/corpus.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Combine & clean text
full_text = " ".join([doc["text"] for doc in articles if "text" in doc])
cleaned_text = clean_text(full_text)

# 3. Perform Linguistic Annotation (POS Tagging & Lemmatization)
print("Annotating text (POS Tagging & Lemmatization across full corpus)...")
pos_counts, words_filtered, lemmas_filtered = annotate_text(cleaned_text, stopwords)

# 4. Calculate Corpus Statistics
total_chars = len(cleaned_text)
total_tokens = len(words_filtered)
unique_types = len(set(words_filtered))

word_freq = get_frequencies(words_filtered)
lemma_freq = get_frequencies(lemmas_filtered)
char_freq = get_char_frequencies(cleaned_text)

# 5. Display Results
print("\n" + "="*50)
print("     SECTION 3 & 4: ANNOTATION & ANALYSIS RESULTS")
print("="*50)
print(f"Total Character Count    : {total_chars:,}")
print(f"Total Clean Tokens       : {total_tokens:,}")
print(f"Unique Word Types        : {unique_types:,}")
print("="*50)

print("\n--- POS TAG DISTRIBUTION ---")
for pos, count in pos_counts.most_common():
    percentage = (count / sum(pos_counts.values())) * 100
    print(f"{pos:<10} : {count:<6} ({percentage:.1f}%)")

print("\n--- TOP 20 MOST FREQUENT WORDS ---")
for word, count in word_freq.most_common(20):
    print(f"{word:<20} : {count}")

print("\n--- TOP 20 MOST FREQUENT LEMMAS ---")
for lemma, count in lemma_freq.most_common(20):
    print(f"{lemma:<20} : {count}")
print("="*50)

print("\n--- TOP 5 MOST FREQUENT CHARACTERS ---")
for char, count in char_freq.most_common(5):
    print(f"{char:<5} : {count}")
print("="*50)