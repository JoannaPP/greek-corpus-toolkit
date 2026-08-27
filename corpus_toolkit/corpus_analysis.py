import re

def calculate_ttr(tokens):
    """Calculates Type-Token Ratio (TTR) for a list of tokens."""
    # Clean punctuation and convert to lowercase
    clean_words = [re.sub(r"[^\w\s]", "", t).lower() for t in tokens if re.sub(r"[^\w\s]", "", t)]
    
    total_tokens = len(clean_words)
    unique_types = len(set(clean_words))
    
    if total_tokens == 0:
        return 0, 0, 0.0
        
    ttr = (unique_types / total_tokens) * 100
    return total_tokens, unique_types, ttr


def get_kwic(tokens, target_word, window=5, max_hits=10):
    """Extracts Key Word In Context (KWIC) concordance lines."""
    target_word = target_word.strip().lower()
    concordances = []
    
    for i in range(len(tokens)):
        clean_word = re.sub(r"[^\w\s]", "", tokens[i]).lower()
        
        if clean_word == target_word:
            left = tokens[max(0, i - window):i]
            right = tokens[i + 1:i + 1 + window]
            
            concordances.append({
                "left": " ".join(left),
                "keyword": tokens[i],
                "right": " ".join(right)
            })
            
            if len(concordances) >= max_hits:
                break
                
    return concordances