#!/usr/bin/env python3
import requests
import json
from pathlib import Path

USER_AGENT = "MidwestSeedCommons/1.0 (student project; learnings.biodistrict@example.com)"
session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "crops"
ASSETS.mkdir(parents=True, exist_ok=True)
CREDITS = ASSETS / "credits.json"
IMG = ASSETS / "tomato.jpg"
OPENVERSE = "https://api.openverse.org/v1/images/"
queries = ["Tipperary Gold Tomato", "Tipperary Gold tomato", "tomato plant", "tomato", "Solanum lycopersicum"]

credits = json.loads(CREDITS.read_text()) if CREDITS.exists() else {}

for q in queries:
    print('Trying Openverse query:', q)
    try:
        r = session.get(OPENVERSE, params={"q": q, "license": "cc0,by", "page_size": 1}, timeout=10)
        r.raise_for_status()
        d = r.json()
        if d.get('results'):
            res = d['results'][0]
            url = res.get('url') or res.get('thumbnail') or res.get('foreign_landing_url')
            if not url:
                continue
            try:
                ir = session.get(url, timeout=15)
                ir.raise_for_status()
                IMG.write_bytes(ir.content)
                credits['tomato'] = {
                    'source': 'Openverse',
                    'title': res.get('title', q),
                    'author': res.get('creator', 'Unknown'),
                    'license': res.get('license', 'Unknown'),
                    'url': res.get('foreign_landing_url', url),
                }
                CREDITS.write_text(json.dumps(credits, indent=2))
                print('Saved new tomato image and updated credits:', credits['tomato'])
                raise SystemExit(0)
            except Exception as e:
                print('Failed to download image at', url, e)
        else:
            print('No results for', q)
    except Exception as e:
        print('Openverse request failed for', q, e)

print('No Openverse image found for tomato')
