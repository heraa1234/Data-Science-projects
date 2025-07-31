from bs4 import BeautifulSoup
import re

# Load your exported HTML file
with open("search-history.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

# Extract text content
queries = []
for div in soup.find_all("div"):
    text = div.get_text(strip=True)
    if text:
        queries.append(text.lower())

# Define keywords that suggest travel intention
travel_keywords = [
    "travel", "trip", "flight", "tour", "places to visit", "vacation",
    "road trip", "hotel", "resort", "itinerary", "backpacking", "hiking",
    "trekking", "beach", "mountain", "city tour", "things to do in", "visa",
    "travel vlog", "explore", "journey", "destinations", "travel guide"
]

# Find queries that match travel-related keywords
travel_queries = [q for q in queries if any(k in q for k in travel_keywords)]

# Print result
if travel_queries:
    print(f"Detected {len(travel_queries)} travel-related queries:")
    for q in travel_queries[:10]:  # show only top 10
        print("•", q)
else:
    print("No clear travel-related intentions found.")
