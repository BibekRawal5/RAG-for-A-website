import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from config import CHUNK_SIZE, CHUNK_OVERLAP

def scrape_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    for script in soup(["script", "style", "noscript"]):
        script.decompose()
    return soup.get_text(separator=" ").strip(), soup

def get_internal_links(soup, base_url, domain):
    links = set()
    for a in soup.find_all("a", href=True):
        href = a['href']
        href = urljoin(base_url, href)
        parsed_href = urlparse(href)
        # Only keep links with same domain and no query or fragment
        if parsed_href.netloc == domain:
            clean_url = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            links.add(clean_url)
    return links

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def crawl_and_chunk(seed_url, max_pages=100, max_depth=5):
    domain = urlparse(seed_url).netloc
    visited = set()
    to_visit = [(seed_url, 0)]  # (url, current_depth)
    all_chunks = []

    while to_visit and len(visited) < max_pages:
        url, depth = to_visit.pop(0)
        if url in visited or depth > max_depth:
            continue

        text, soup = scrape_text(url)
        if text:
            chunks = chunk_text(text)
            all_chunks.extend(chunks)
            visited.add(url)

            if depth < max_depth:
                links = get_internal_links(soup, url, domain)
                for link in links:
                    if link not in visited and all(link != u for u, _ in to_visit):
                        to_visit.append((link, depth + 1))

    return all_chunks
