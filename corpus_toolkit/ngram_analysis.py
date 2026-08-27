from collections import Counter

def analyze_ngrams(tokens, top_n=10):
    unigrams = Counter(tokens).most_common(top_n)
    
    bigrams = [" ".join(tokens[i:i+2]) for i in range(len(tokens) - 1)]
    top_bigrams = Counter(bigrams).most_common(top_n)
    
    trigrams = [" ".join(tokens[i:i+3]) for i in range(len(tokens) - 2)]
    top_trigrams = Counter(trigrams).most_common(top_n)
    
    return unigrams, top_bigrams, top_trigrams