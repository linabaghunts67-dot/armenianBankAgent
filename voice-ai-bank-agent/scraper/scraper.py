"""
scraper.py — Scrapes credits, deposits, and branch location data from 3 Armenian banks:
  1. Ameriabank   — https://www.ameriabank.am
  2. Ardshinbank  — https://www.ardshinbank.am
  3. ACBA Bank    — https://www.acba.am

Run to regenerate data/bank_data.json:
  python scraper/scraper.py
"""

import json
import os
import time
import requests
from bs4 import BeautifulSoup

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bank_data.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

SCRAPE_TARGETS = [
    # Ameriabank
    {"bank": "Ameriabank", "topic": "credits", "url": "https://www.ameriabank.am/page.aspx?id=285&lang=2", "source": "https://www.ameriabank.am"},
    {"bank": "Ameriabank", "topic": "deposits", "url": "https://www.ameriabank.am/page.aspx?id=270&lang=2", "source": "https://www.ameriabank.am"},
    {"bank": "Ameriabank", "topic": "branch_locations", "url": "https://www.ameriabank.am/page.aspx?id=16&lang=2", "source": "https://www.ameriabank.am"},
    # Ardshinbank
    {"bank": "Ardshinbank", "topic": "credits", "url": "https://www.ardshinbank.am/am/individuals/loans/", "source": "https://www.ardshinbank.am"},
    {"bank": "Ardshinbank", "topic": "deposits", "url": "https://www.ardshinbank.am/am/individuals/deposits/", "source": "https://www.ardshinbank.am"},
    {"bank": "Ardshinbank", "topic": "branch_locations", "url": "https://www.ardshinbank.am/am/about/branches/", "source": "https://www.ardshinbank.am"},
    # ACBA Bank
    {"bank": "ACBA Bank", "topic": "credits", "url": "https://www.acba.am/hy/individuals/loans", "source": "https://www.acba.am"},
    {"bank": "ACBA Bank", "topic": "deposits", "url": "https://www.acba.am/hy/individuals/deposits", "source": "https://www.acba.am"},
    {"bank": "ACBA Bank", "topic": "branch_locations", "url": "https://www.acba.am/hy/about/branches", "source": "https://www.acba.am"},
]


def scrape_page(url: str) -> str:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return " ".join(lines[:200])
    except Exception as e:
        print(f" !!!!  Failed to scrape {url}: {e}")
        return ""


def run_scraper():
    print("Scraping Armenian bank websites...\n")
    results = []

    for target in SCRAPE_TARGETS:
        print(f"  → {target['bank']} / {target['topic']} ...")
        content = scrape_page(target["url"])
        if content:
            results.append({
                "bank": target["bank"],
                "topic": target["topic"],
                "content": content,
                "source": target["source"],
            })
            print(f"{len(content)} chars scraped")
        else:
            print(f"No content scraped")
        time.sleep(1.5)

    if results:
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nSaved {len(results)} entries to {OUTPUT_PATH}")
    else:
        print("\nNo data scraped.")


if __name__ == "__main__":
    run_scraper()
