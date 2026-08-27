import json
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

class CorpusScraper:
    """Scrapes structured web texts and preserves corpus metadata."""
    
    def __init__(self, headers=None):
        self.headers = headers or {'User-Agent': 'Mozilla/5.0'}

    def get_links_from_page(self, main_url):
        """Finds all article links on a page automatically."""
        req = Request(main_url, headers=self.headers)
        html = urlopen(req).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, "html.parser")
        
        found_links = set()
        for link in soup.find_all("a", href=True):
            url = link["href"]
            if url.startswith("http"):
                found_links.add(url)
                
        return list(found_links)

    def scrape_url(self, url, genre="News", license_type="Academic"):
        """Fetches a URL, extracts article content, and structures text with metadata."""
        req = Request(url, headers=self.headers)
        html = urlopen(req).read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else "Untitled"
        
        # Target main article container to bypass footers
        article_body = soup.find("article") or soup.find("div", class_=re.compile(r"content|article|entry|post", re.I))
        
        if article_body:
            paragraphs = article_body.find_all("p")
        else:
            paragraphs = soup.find_all("p")

        cleaned_paragraphs = []
        for p in paragraphs:
            p_text = p.get_text(" ", strip=True)
            # Skip noise and short promotional fragments
            if len(p_text) < 40 or "portal ψυχαγωγίας" in p_text or "Γίνετε συνδρομητής" in p_text:
                continue
            cleaned_paragraphs.append(p_text)

        raw_text = " ".join(cleaned_paragraphs)
        cleaned_text = re.sub(r'\s+', ' ', raw_text)
        cleaned_text = re.sub(r'https?://[^\s]*', '', cleaned_text)
        
        token_count = len(cleaned_text.split())

        return {
            "title": title,
            "source": url,
            "author": "Unknown",
            "year": 2026,
            "genre": genre,
            "license": license_type,
            "token_count": token_count,
            "text": cleaned_text
        }

    def save_corpus_to_json(self, documents, output_filepath):
        """Saves a collection of structured documents into a JSON file."""
        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(documents, f, ensure_ascii=False, indent=4)