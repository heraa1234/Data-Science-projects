import os
import json
import spacy
from bs4 import BeautifulSoup
from collections import Counter

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Travel-related keywords
travel_keywords = [
    "travel", "trip", "tour", "flight", "vacation", "holiday", "resort", "destination",
    "explore", "places to visit", "tourist", "road trip", "itinerary", "beach", "mountain",
    "hotel", "airbnb", "trek", "backpacking", "weekend getaway", "staycation", "visa",
    "booking", "airlines", "cruise", "adventure", "tourism", "sightseeing", "coimbatore",
    "goa", "delhi", "paris", "new york", "london", "kerala", "europe", "usa", "canada",
    "thailand", "singapore", "japan", "malaysia"
]

def contains_travel_intent(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in travel_keywords)

def parse_youtube_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    entries = []
    for tag in soup.find_all("div"):
        content = tag.get_text(separator=" ", strip=True)
        if content and contains_travel_intent(content):
            entries.append(("youtube", content))
    return entries

def parse_google_html(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    entries = []
    for tag in soup.find_all("div"):
        content = tag.get_text(separator=" ", strip=True)
        if content and contains_travel_intent(content):
            entries.append(("google", content))
    return entries

def parse_chrome_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    entries = []
    for item in data.get("Browser History", []):
        url = item.get("url", "")
        title = item.get("title", "")
        combined = f"{title} {url}"
        if contains_travel_intent(combined):
            entries.append(("chrome", combined))
    return entries

def extract_locations(entries):
    location_counter = Counter()
    for _, text in entries:
        if len(text) > 1000000:
            continue  # skip too long
        doc = nlp(text[:10000])  # limit size
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:
                location_counter[ent.text.strip()] += 1
    return location_counter.most_common(10)

def main():
    print("📂 Travel Intent Detection Summary\n")

    # File paths
    youtube_file = "search-history.html"
    google_file = "Google_Search_history.html"
    chrome_file = "History.json"

    # Collect all results
    all_results = []

    if os.path.exists(youtube_file):
        yt_results = parse_youtube_html(youtube_file)
        watch_count = len([r for r in yt_results if "watched" in r[1].lower()])
        search_count = len([r for r in yt_results if "searched" in r[1].lower()])
        print(f"YouTube Watch: Found {watch_count} travel-related entries.")
        print(f"\nYouTube Search: Found {search_count} travel-related entries.\n")
        all_results.extend(yt_results)

    if os.path.exists(google_file):
        google_results = parse_google_html(google_file)
        print(f"Google Search: Found {len(google_results)} travel-related entries.\n")
        all_results.extend(google_results)

    if os.path.exists(chrome_file):
        chrome_results = parse_chrome_json(chrome_file)
        print(f" Chrome: Found {len(chrome_results)} travel-related entries.\n")
        all_results.extend(chrome_results)

    # Display totals
    print(f"Total travel-related entries: {len(all_results)}\n")

    # Show destination guesses
    print("Possible Travel Destinations Mentioned:")
    locations = extract_locations(all_results)
    if locations:
        for loc, count in locations:
            print(f"• {loc} ({count} mentions)")
    else:
        print("No clear travel locations detected.")

if __name__ == "__main__":
    main()
