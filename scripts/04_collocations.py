import json
from collections import Counter
from corpus_toolkit.preprocessor import clean_text
from corpus_toolkit.collocations import extract_tokens, get_collocations

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
print("Extracting lemmas...")
tokens = extract_tokens(cleaned_text, stopwords)

# Count unigrams and bigrams
unigram_counts = Counter(tokens)
bigram_counts = Counter(zip(tokens[:-1], tokens[1:]))
total_bigrams = sum(bigram_counts.values())

def print_collocations(target_word, top_n=10):
    target_word = target_word.strip().lower()
    f_x = unigram_counts[target_word]
    
    if f_x == 0:
        print(f"\nWord '{target_word}' was not found in the corpus.")
        return

    results = get_collocations(target_word, unigram_counts, bigram_counts, total_bigrams)

    if not results:
        print(f"\nNo collocations found for '{target_word}' above the minimum frequency threshold.")
        return

    print("\n" + "="*80)
    print(f" COLLOCATION ANALYSIS FOR TARGET WORD: '{target_word.upper()}' (Frequency: {f_x})")
    print("="*80)
    print(f"{'Bigram Pair':<30} | {'Freq (O)':<8} | {'MI':<8} | {'t-score':<8} | {'Dice':<8} | {'Log-Likelihood':<12}")
    print("-" * 80)
    
    for item in results[:top_n]:
        print(f"{item['bigram']:<30} | {item['O']:<8} | {item['MI']:<8.2f} | {item['t-score']:<8.2f} | {item['Dice']:<8.3f} | {item['LL']:<12.2f}")
    print("="*80)

# Interactive Prompt for Custom Input
print("\n--- COLLOCATION SEARCH ---")
user_input = input("Enter a Greek word to analyze (or press ENTER to run default 'ελλάδα' & 'κυβέρνηση'): ")

if user_input.strip():
    print_collocations(user_input)
else:
    # Default fallback demo
    print_collocations("ελλάδα", top_n=10)
    print_collocations("κυβέρνηση", top_n=10)