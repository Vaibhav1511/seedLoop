#!/usr/bin/env python3
import requests
import json
from pathlib import Path

USER_AGENT = "MidwestSeedCommons/1.0 (student project; learnings.biodistrict@example.com)"
session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets" / "crops"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)
CREDITS_PATH = ASSETS_DIR / "credits.json"
IMAGE_PATH = ASSETS_DIR / "purple_sprouting_broccoli.jpg"

OPENVERSE_URL = "https://api.openverse.org/v1/images/"
queries = ["purple sprouting broccoli", "broccoli"]

def load_credits():
    if CREDITS_PATH.exists():
        return json.loads(CREDITS_PATH.read_text())
    return {}

def save_credits(c):
    CREDITS_PATH.write_text(json.dumps(c, indent=2))

def try_openverse(q):
    try:
        params = {"q": q, "license": "cc0,by", "page_size": 1}
        r = session.get(OPENVERSE_URL, params=params, timeout=10)
        r.raise_for_status()
        d = r.json()
        if d.get("results"):
            res = d["results"][0]
            image_url = res.get("url") or res.get("thumbnail") or res.get("foreign_landing_url")
            if image_url:
                try:
                    img = session.get(image_url, timeout=15)
                    img.raise_for_status()
                    with open(IMAGE_PATH, "wb") as f:
                        f.write(img.content)
                    credits = load_credits()
                    credits["purple_sprouting_broccoli"] = {
                        "source": "Openverse",
                        "title": res.get("title", q),
                        "author": res.get("creator", "Unknown"),
                        "license": res.get("license", "Unknown"),
                        "url": res.get("foreign_landing_url", image_url),
                    }
                    save_credits(credits)
                    print(f"Downloaded via Openverse: {res.get('title')}")
                    return True
                except Exception as e:
                    print("Openverse image download failed:", e)
        else:
            print("Openverse: no results for", q)
    except Exception as e:
        print("Openverse request failed for", q, e)
    return False


def try_wikipedia(qs):
    for q in qs:
        try:
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{q}"
            wr = session.get(wiki_url, timeout=10)
            wr.raise_for_status()
            wd = wr.json()
            orig = wd.get("originalimage")
            if orig and orig.get("source"):
                wiki_image_url = orig["source"]
                headers = {"User-Agent": USER_AGENT, "Referer": "https://www.wikipedia.org/"}
                img = requests.get(wiki_image_url, headers=headers, timeout=15)
                img.raise_for_status()
                with open(IMAGE_PATH, "wb") as f:
                    f.write(img.content)
                credits = load_credits()
                credits["purple_sprouting_broccoli"] = {
                    "source": "Wikimedia Commons",
                    "title": wd.get("title", q),
                    "author": "Unknown (Wikimedia Commons)",
                    "license": "See Wikimedia page",
                    "url": wiki_image_url,
                }
                save_credits(credits)
                print("Downloaded via Wikimedia:", wd.get("title"))
                return True
        except Exception as e:
            print("Wikipedia fallback failed for", q, e)
    return False

if __name__ == '__main__':
    success = False
    for q in queries:
        if try_openverse(q):
            success = True
            break
    if not success:
        if try_wikipedia(queries):
            success = True
    if success:
        print("purple_sprouting_broccoli image updated and credits.json modified.")
    else:
        print("Failed to retrieve purple_sprouting_broccoli image via Openverse/Wikipedia.")
