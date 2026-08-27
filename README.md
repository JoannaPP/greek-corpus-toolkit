Student: Ioanna Pepa  
Matriculation number: 01/1591952  
Course: Corpus Linguistics with Python  
Module: 2nd  
Lecturer: Ph.D. Sarveswaran Kengatharaiyer  
Tutor: Francesca Hoffmeier  
Semester: Summer 2026  

# Greek News-Articles Corpus Toolkit

**Repository:** https://github.com/JoannaPP/greek-corpus-toolkit

The current Python toolkit builds and analyzes a Modern Greek news-articles corpus. It handles scraping, cleaning, tokenising, POS tagging/lemmatising, computing frequencies and collocations, word-searching and n-gram analysis.

## Project overview

This project collects a corpus of Modern Greek news-articles from the web and provides a small toolkit to analyse it: word and character frequencies, Type-Token Ratio, KWIC concordances, keyword/regex/POS search, collocation statistics (MI, t-score, Dice, Log-Likelihood) and n-grams. Linguistic annotation (POS tagging and lemmatisation) is done with spaCy's Greek model `el_core_news_sm`.

## Data collection approach

Articles are scraped from three Greek news-articles websites across several section pages like society, politics, world, culture, etc.:  
1. [Naftemporiki](https://www.naftemporiki.gr) (business/finance)  
2. [ERT News](https://www.ertnews.gr) (the Greek public broadcaster)  
3. [Kathimerini](https://www.kathimerini.gr) (a Greek daily newspaper)

The scraper first collects all article links from each section page, then visits each article and extracts the main text while skipping short/promotional fragments (e.g. subscription prompts, navigation text). Each article is stored with metadata (title, source URL, author, year, genre, license, token count) and saved to `data/corpus.json`. The collection stops once the corpus reaches roughly 100,000 tokens, as required by the assignment.

## System architecture / design decisions

I split the code into two parts:  
1. a package called `corpus_toolkit/`  
2. a `scripts/` folder  

The `corpus_toolkit/` package contains all the functions that do the work. There is one file with defined functions per component from the assignment (scraping, preprocessing, annotation, collocations, corpus analysis, word-search, n-grams). Each script loads the corpus from `data/corpus.json`, calls the relevant functions from the toolkit, and prints the results to the terminal.
I did it this way instead of writing seven standalone scripts because a few of the components need the same processing. For example, the tokenising/lemmatising step in `collocations.py` is reused by `ngram_analysis.py`, so I only wrote that logic once instead of copying it into two files. It also keeps each file organised and focused on one thing.

| Module | Responsibility |
|---|---|
| `scraper.py` | Collects article links, scrapes article text + metadata, saves corpus to JSON |
| `preprocessor.py` | Text cleaning, sentence splitting, and stopword-filtered tokenisation (spaCy) |
| `annotation.py` | POS tagging and lemmatisation, POS counts, TTR, word/lemma/character frequency (spaCy + NLTK `FreqDist`) |
| `collocations.py` | Lemma extraction and bigram collocation statistics: MI, t-score, Dice, Log-Likelihood |
| `corpus_analysis.py` | TTR on raw tokens, KWIC concordance search |
| `corpus_search.py` | Keyword, regex, and POS-tag search over the corpus |
| `ngram_analysis.py` | Unigram, bigram, and trigram frequency counts |

A few design notes:

- **spaCy over NLTK**: it includes a trained Greek model (`el_core_news_sm`) that handles sentence segmentation, tokenisation, POS tagging, and lemmatisation together, which NLTK doesn't provide for Greek.
- **Custom stopword list** (`data/stopwords_el.json`): a self-built list of Modern Greek function words (articles, pronouns, conjunctions, prepositions, etc.), since the existing lists did not cover what was needed.

## Installation

```bash
git clone https://github.com/JoannaPP/greek-corpus-toolkit.git
cd greek-corpus-toolkit
pip install -r requirements.txt
python -m spacy download el_core_news_sm
```

## Usage

Run the `scripts/` in this given order, since each upcoming stage reads `data/corpus.json` produced by the `01_scraper.py`:

```bash
python scripts/01_scraper.py      # builds data/corpus.json from the news-articles websites
python scripts/02_preprocessor.py         # cleaning + tokenisation
python scripts/03_annotation.py           # POS tagging, lemmatisation, frequencies
python scripts/04_collocations.py       # collocation statistics for a chosen word
python scripts/05_corpus_analysis.py    # TTR + KWIC concordance search
python scripts/06_corpus_search.py             # keyword / regex / POS search
python scripts/07_ngram_analysis.py             # unigram / bigram / trigram frequencies
```

Several scripts (`04_collocations.py`, `05_corpus_analysis.py`, `06_corpus_search.py`) are prompted for an interactive input. The user can either press *Enter* to run the built-in code (e.g. searching *ελλάδα* and *κυβέρνηση*) or copy-paste one of the words that appear at the print-message or type their own word.

## Example commands and outputs

Example command 1:

```bash
python scripts/04_collocations.py
> Enter a Greek word to analyze (or press ENTER to run default 'ελλάδα' & 'κυβέρνηση'): κυβέρνηση
```

Example output 1:

```
================================================================================
 COLLOCATION ANALYSIS FOR TARGET WORD: 'ΚΥΒΈΡΝΗΣΗ' (Frequency: 112)
================================================================================
Bigram Pair                    | Freq (O) | MI       | t-score  | Dice| Log-Likelihood
--------------------------------------------------------------------------------
κυβέρνηση τραμπ                | 7        | 6.88     | 2.62     | 0.101| 66.78       
αμερικάνικος κυβέρνηση         | 3        | 5.77     | 1.70     | 0.044| 24.00       
κυβέρνηση επιχειρώ             | 3        | 5.77     | 1.70     | 0.044| 24.00       
κυβέρνηση πασοκ                | 3        | 5.20     | 1.69     | 0.040| 21.65       
κυβέρνηση θέλω                 | 3        | 4.92     | 1.67     | 0.038| 20.47       
ελληνικός κυβέρνηση            | 4        | 3.69     | 1.85     | 0.032| 20.46       
κυβέρνηση ηπα                  | 3        | 4.07     | 1.63     | 0.031| 16.94       
πολιτική κυβέρνηση             | 3        | 3.69     | 1.60     | 0.028| 15.33       
αγορά κυβέρνηση                | 3        | 3.25     | 1.55     | 0.024| 13.53       
================================================================================
```
Example command 2:

```bash
python scripts/05_corpus_analysis.py
> Enter a Greek word to search (or press ENTER for default 'ελλάδα' & 'κυβέρνηση'): Ελλάδα
```

Example output 2:

```
================================================================================
 KWIC CONCORDANCE SEARCH FOR: 'ΕΛΛΆΔΑ' (Showing up to 10 hits)
================================================================================
           «το πιο σύγχρονο Μετρό στην |  Ελλάδα»   | και «ένα από τα πιο                   
    την αίσθηση που καλλιεργείται στην |   Ελλάδα   | πως οι ομογενείς «λύνουν και          
              οποίων «οι δεσμοί με την |   Ελλάδα   | είναι κυρίως οι καλοκαιρινές διακοπές»
   από το ισραηλινό». Συμπέρασμα: στην |   Ελλάδα   | ζούμε πολλές φορές με μύθους.         
               το 2030», με στόχο «μια |   Ελλάδα   | πιο ισχυρή και πιο παραγωγική».       
     τα τελευταία χρόνια έρχονται στην |   Ελλάδα   | ξένοι, μέλη εγκληματικών ομάδων, ενώ  
     αποτύπωση πραγμάτων, ακούμε ότι η |   Ελλάδα   | είναι η ακριβότερη χώρα με            
              ότι το επίπεδο ζωής στην |   Ελλάδα   | είναι χαμηλότερο από τη Βουλγαρία.    
           μεγεθών, τη στιγμή που στην |  Ελλάδα,   | με τις θυσίες των πολιτών             
              2019 είναι 12,7% για την |  Ελλάδα,   | όταν στο μέσο όρο της                 
================================================================================
```

Example command 3:

```bash
python scripts/06_corpus_search.py
> EEnter a POS tag (e.g., NOUN, VERB, ADJ, PROPN) or press ENTER to skip: adj
```

Example output 3:

```
--- POS TAG SEARCH RESULTS ---
POS Tag              : 'ADJ'
Total occurrences    : 9436
Sample matches       : ['εσωτερικά', 'εντυπωσιακό', 'εξευτελισμένες', 'νέους', 'πλήρη', 'Περισσότερες', 'δύσκολα', 'ορισμένες', 'γνωστό', 'μεγαλύτερες']
```

## Corpus description

- **Language**: Modern Greek (el)
- **Genre**: News-Articles
- **Sources**: naftemporiki.gr, ertnews.gr, kathimerini.gr
- **Size**: ~100,000 tokens (target set in `scrape_corpus.py`)
- **Format**: JSON, one entry per article, with `title`, `source`, `author`, `year`, `genre`, `license`, `token_count`, and `text` fields

## Challenges faced

- **Inconsistent HTML structure across news-articles websites**: Each website marks up its article body differently, so the scraper looks for an `<article>` tag or a `<div>` with a class matching `content|article|entry|post`. If neither is found, it looks for all `<p>` tags.
- **Filtering out non-article text**: Article pages contain a lot of promotional text or links that navigate the reader to a differeent page. These had to be filtered out by length and by matching known boilerplate phrases.
- **Stopword list**: I did not dind a decent stopword list for Modern Greek that could cover everything needed, so I had to create my own `stopwords_el.json` list.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.