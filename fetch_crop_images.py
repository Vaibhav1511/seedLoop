import requests
import json
import os
from pathlib import Path

# User-Agent header for API requests
USER_AGENT = "MidwestSeedCommons/1.0 (student project; learnings.biodistrict@example.com)"

# Create a session with persistent headers
session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

# Map seeds to crop queries
SEED_QUERIES = {
    "carrot": "Daucus carota",
    "oat": "Avena sativa",
    "runner_bean": "Phaseolus coccineus",
    "lovage": "Levisticum officinale",
    "purple_sprouting_broccoli": "Brassica oleracea",
    "tomato": "Solanum lycopersicum",
}
import requests
import json
from pathlib import Path

# User-Agent header for API requests
USER_AGENT = "MidwestSeedCommons/1.0 (student project; learnings.biodistrict@example.com)"

# Create a session with persistent headers
session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

# Map seeds to crop queries
SEED_QUERIES = {
    "carrot": "Daucus carota",
    "oat": "Avena sativa",
    "runner_bean": "Phaseolus coccineus",
    "lovage": "Levisticum officinale",
    "purple_sprouting_broccoli": "Brassica oleracea",
    "tomato": "Solanum lycopersicum",
}

# Fallback queries if primary fails (simpler/common-name queries)
FALLBACK_QUERIES = {
    "oat": "oat",
    "lovage": "lovage",
}

ASSETS_DIR = Path(__file__).parent / "assets" / "crops"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

credits = {}
successful = []

OPENVERSE_URL = "https://api.openverse.org/v1/images/"

for seed_id, primary_query in SEED_QUERIES.items():
    print(f"Fetching image for {seed_id} (query: {primary_query})...")
    image_path = ASSETS_DIR / f"{seed_id}.jpg"

    # Build list of queries to try: primary first, then fallback if present
    queries_to_try = [primary_query]
    if seed_id in FALLBACK_QUERIES:
        queries_to_try.append(FALLBACK_QUERIES[seed_id])

    got_image = False

    for q in queries_to_try:
        try:
            params = {"q": q, "license": "cc0,by", "page_size": 1}
            resp = session.get(OPENVERSE_URL, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            if data.get("results"):
                result = data["results"][0]
                # Prefer a direct file URL if available, else use landing url
                image_url = result.get("url") or result.get("thumbnail") or result.get("foreign_landing_url")
                if image_url:
                    try:
                        img = session.get(image_url, timeout=15)
                        img.raise_for_status()
                        with open(image_path, "wb") as f:
                            f.write(img.content)

                        credits[seed_id] = {
                            "source": "Openverse",
                            "title": result.get("title", "Unknown"),
                            "author": result.get("creator", "Unknown"),
                            "license": result.get("license", "Unknown"),
                            "url": result.get("foreign_landing_url", image_url),
                        }
                        print(f"  ✓ Downloaded from Openverse (query='{q}'): {result.get('title')}")
                        successful.append(seed_id)
                        got_image = True
                        break
                    except requests.exceptions.RequestException as e:
                        print(f"  ✗ Failed to download image from Openverse URL: {e}")
                        # try next query or fallback
            else:
                print(f"  ✗ Openverse: no results for query '{q}'")
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Openverse request failed for query '{q}': {e}")

    if got_image:
        continue

    # Try Wikipedia / Wikimedia fallback using page summary originalimage
    try:
        print(f"  Trying Wikipedia fallback for '{primary_query}'...")
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{primary_query}"
        wiki_resp = session.get(wiki_url, timeout=10)
        wiki_resp.raise_for_status()
        wiki_data = wiki_resp.json()

        orig = wiki_data.get("originalimage")
        if orig and orig.get("source"):
            wiki_image_url = orig["source"]
            # Wikimedia often requires a Referer header
            headers = {"User-Agent": USER_AGENT, "Referer": "https://www.wikipedia.org/"}
            try:
                img = requests.get(wiki_image_url, headers=headers, timeout=15)
                img.raise_for_status()
                with open(image_path, "wb") as f:
                    f.write(img.content)

                credits[seed_id] = {
                    "source": "Wikimedia Commons",
                    "title": wiki_data.get("title", primary_query),
                    "author": "Unknown (Wikimedia Commons)",
                    "license": "See Wikimedia page",
                    "url": wiki_image_url,
                }
                print(f"  ✓ Downloaded from Wikimedia Commons: {wiki_data.get('title')}")
                successful.append(seed_id)
                got_image = True
            except requests.exceptions.RequestException as e:
                print(f"  ✗ Wikimedia image download failed (likely protected): {e}")
        else:
            print(f"  ✗ Wikipedia summary had no originalimage for '{primary_query}'")
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Wikipedia request failed for '{primary_query}': {e}")

    if not got_image:
        print(f"  ✗ Could not fetch an image for {seed_id}")

# Write credits file
credits_path = ASSETS_DIR / "credits.json"
with open(credits_path, "w") as f:
    json.dump(credits, f, indent=2)

print("\n" + "=" * 50)
print(f"Successfully fetched {len(successful)} / {len(SEED_QUERIES)} images:")
for s in successful:
    print(f"  ✓ {s}")
print(f"Credits written to: {credits_path}")
print("" + "=" * 50)
