import json
import re
from corpus_toolkit.corpus_analysis import calculate_ttr, get_kwic

# Load corpus dataset
print("Loading corpus dataset...")
with open("data/corpus.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Extract raw tokens
full_text = " ".join([doc["text"] for doc in articles if "text" in doc])
tokens = [t for t in re.split(r"\s+", full_text) if t]

# Calculate and display TTR
total_tokens, unique_types, ttr_score = calculate_ttr(tokens)

print("\n" + "="*80)
print(" CORPUS OVERVIEW & TYPE-TOKEN RATIO (TTR)")
print("="*80)
print(f"Total Tokens (N)  : {total_tokens:,}")
print(f"Unique Types (V)  : {unique_types:,}")
print(f"TTR Score         : {ttr_score:.2f}%")
print("="*80)

def print_kwic_results(target_word, window=5, max_hits=10):
    results = get_kwic(tokens, target_word, window=window, max_hits=max_hits)
    
    print("\n" + "="*80)
    print(f" KWIC CONCORDANCE SEARCH FOR: '{target_word.upper()}' (Showing up to {max_hits} hits)")
    print("="*80)
    
    if not results:
        print(f"No occurrences found for '{target_word}' in the corpus.")
        print("="*80)
        return
        
    for item in results:
        left_str = item["left"]
        keyword = item["keyword"]
        right_str = item["right"]
        print(f"{left_str:>38} | {keyword:^10} | {right_str:<38}")
        
    print("="*80)

# Interactive Prompt for KWIC
print("\n--- KWIC CONCORDANCE SEARCH ---")
user_input = input("Enter a Greek word to search (or press ENTER for default 'ελλάδα' & 'κυβέρνηση'): ")

if user_input.strip():
    print_kwic_results(user_input)
else:
    # Default fallback demo
    print_kwic_results("ελλάδα")
    print_kwic_results("κυβέρνηση")