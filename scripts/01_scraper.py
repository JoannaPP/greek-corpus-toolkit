from corpus_toolkit.scraper import CorpusScraper

scraper = CorpusScraper()

# List of section pages to try gathering links from
category_urls = [
    "https://www.naftemporiki.gr/society/",
    "https://www.naftemporiki.gr/finance/",
    "https://www.naftemporiki.gr/politics/",
    "https://www.naftemporiki.gr/world/",
    "https://www.ertnews.gr/katigories/ellada/",
    "https://www.ertnews.gr/katigories/kosmos/",
    "https://www.kathimerini.gr/society/",
    "https://www.kathimerini.gr/politics/",
    "https://www.kathimerini.gr/culture/"
]

print("Automatically gathering article links from multiple sections...")
all_links = set()

for category in category_urls:
    try:
        links = scraper.get_links_from_page(category)
        all_links.update(links)
        print(f"Collected links from: {category}")
    except Exception as e:
        # If a section gives a 404 or fails, skip it smoothly!
        print(f"Skipping {category} (Error: {e})")

print(f"\nTotal unique article links found: {len(all_links)}")

documents = []
total_words = 0
TARGET_TOKENS = 100000

for url in all_links:
    if total_words >= TARGET_TOKENS:
        print(f"\nGoal reached! Total words collected: {total_words}")
        break

    try:
        doc = scraper.scrape_url(url, genre="News", license_type="Academic")
        
        if doc["token_count"] > 50:
            documents.append(doc)
            total_words += doc["token_count"]
            print(f"Scraped: {doc['title'][:35]}... | Words: {doc['token_count']} | Total: {total_words}/{TARGET_TOKENS}")
            
    except Exception:
        continue

scraper.save_corpus_to_json(documents, "data/corpus.json")
print(f"Done! Saved {len(documents)} articles with {total_words} total words to data/corpus.json")