import re

def search_keyword(doc, target_word, limit=5):
    """Searches for exact surface matches of a target word."""
    target_lower = target_word.strip().lower()
    matches = [token.text for token in doc if token.text.lower() == target_lower]
    return len(matches), matches[:limit]


def search_regex(doc, pattern_str, limit=5):
    """Searches tokens using a regular expression pattern."""
    try:
        pattern = re.compile(pattern_str)
        matches = [token.text for token in doc if pattern.search(token.text)]
        return len(matches), matches[:limit]
    except re.error:
        return 0, []


def search_by_pos(doc, pos_tag, limit=10):
    """Finds tokens matching a specific POS tag (e.g., NOUN, VERB, ADJ)."""
    pos_tag = pos_tag.strip().upper()
    matches = [token.text for token in doc if token.pos_ == pos_tag]
    return len(matches), matches[:limit]