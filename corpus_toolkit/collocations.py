import math
import re
import spacy

nlp = spacy.load("el_core_news_sm")

def extract_tokens(text, stopwords):
    """Tokenizes text into Greek lemmas, skipping punctuation and stopwords."""
    nlp.max_length = len(text) + 1000
    doc = nlp(text)
    
    tokens = []
    for token in doc:
        if token.is_punct or token.is_space:
            continue
        
        lemma = token.lemma_.lower()
        
        # Split multi-word lemmas (like "σε ο") and check each word against stopwords
        lemma_parts = lemma.split()
        if all(re.search(r"[α-ωΑ-Ωά-ώ]", p) and p not in stopwords for p in lemma_parts):
            tokens.append(lemma)
            
    return tokens


def get_collocations(target_word, unigram_counts, bigram_counts, total_bigrams, min_freq=3):
    """Calculates MI, t-score, Dice, and Log-Likelihood for a target word."""
    f_x = unigram_counts[target_word]
    if f_x == 0:
        return []

    results = []

    for (w1, w2), O in bigram_counts.items():
        if O < min_freq:
            continue
        
        # Check if target_word is in the bigram
        if w1 == target_word:
            other_word = w2
        elif w2 == target_word:
            other_word = w1
        else:
            continue
        
        f_y = unigram_counts[other_word]
        N = total_bigrams
        
        # Expected frequency
        E = (f_x * f_y) / N
        
        # 1. Mutual Information (MI)
        mi = math.log2((O * N) / (f_x * f_y))
        
        # 2. t-score
        t_score = (O - E) / math.sqrt(O)
        
        # 3. Dice Coefficient
        dice = (2 * O) / (f_x + f_y)
        
        # 4. Log-Likelihood (LL)
        ll = 2 * O * math.log(O / E) if E > 0 else 0
        
        results.append({
            "bigram": f"{w1} {w2}",
            "O": O,
            "MI": mi,
            "t-score": t_score,
            "Dice": dice,
            "LL": ll
        })

    # Sort results by Log-Likelihood
    results.sort(key=lambda x: x["LL"], reverse=True)
    return results