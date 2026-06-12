import pandas as pd
import json
from pathlib import Path

# Attach image paths and credits from assets/crops/credits.json when available
ASSETS_DIR = Path(__file__).parent / "assets" / "crops"
_credits_path = ASSETS_DIR / "credits.json"
_credits = {}
if _credits_path.exists():
    try:
        _credits = json.loads(_credits_path.read_text())
    except Exception:
        _credits = {}

SEEDS = {
    "Autumn King Carrot": {
        "crop": "Root", "sci": "Daucus carota",
        "note": "Late maincrop carrot rescued from the national collection and re-adapted to the heavier soils of the lower Shannon.",
        "lineage": [
            {"year": 2019, "stage": "Origin",  "place": "Irish Seed Savers Collection", "grower": "Capparoe, Scariff", "county": "Clare",     "lat": 52.908, "lon": -8.531, "gen": "Gen 0", "adapt": "Released from the national seed bank for on-farm revival."},
            {"year": 2021, "stage": "Past",    "place": "Raheen Market Garden",         "grower": "Máire Ó'Brien",     "county": "Limerick",  "lat": 52.620, "lon": -8.660, "gen": "Gen 1", "adapt": "Selected for tolerance of heavy, wet estuary ground."},
            {"year": 2023, "stage": "Past",    "place": "Cloughjordan Community Farm",  "grower": "Pádraig Flynn",     "county": "Tipperary", "lat": 52.951, "lon": -8.030, "gen": "Gen 3", "adapt": "Roots ran straighter on free-draining soil."},
            {"year": 2025, "stage": "Current", "place": "Gort Walled Garden",           "grower": "Aoife Kavanagh",    "county": "Galway",    "lat": 53.069, "lon": -8.819, "gen": "Gen 4", "adapt": "Sown in succession for a long autumn harvest."},
            {"year": 2025, "stage": "Current", "place": "Ennis Allotments",             "grower": "Siobhán Murphy",    "county": "Clare",     "lat": 52.843, "lon": -8.989, "gen": "Gen 4", "adapt": "Shared back to new entrants at the spring swap."},
        ],
        "quantity_kg": 1.2,
        "price": "€12/kg",
        "availability": "Available now",
        "organic": True,
        "royalty_status": "Open — royalty-free in the Commons",
    },
    "Wexford Heritage Oat": {
        "crop": "Grain", "sci": "Avena sativa",
        "note": "A tall landrace oat carried west from the south-east. Straw for thatch and bedding; grain mills to a nutty porridge.",
        "lineage": [
            {"year": 2018, "stage": "Origin",  "place": "Family seed line",     "grower": "Carried from Co. Wexford", "county": "Tipperary", "lat": 52.860, "lon": -8.200, "gen": "Heirloom", "adapt": "Entrusted to the Commons by a retiring tillage farmer."},
            {"year": 2022, "stage": "Past",    "place": "Nenagh Tillage Plot",  "grower": "Pádraig Flynn",            "county": "Tipperary", "lat": 52.864, "lon": -8.198, "gen": "Gen 2",    "adapt": "Re-acclimatised to the wetter midlands climate."},
            {"year": 2024, "stage": "Current", "place": "Loughrea Co-op Field", "grower": "Brigid Ní Fhaoláin",      "county": "Galway",    "lat": 53.198, "lon": -8.566, "gen": "Gen 3",    "adapt": "Lodging reduced by selecting shorter, stiffer straw."},
            {"year": 2025, "stage": "Current", "place": "Raheen Market Garden", "grower": "Máire Ó'Brien",           "county": "Limerick",  "lat": 52.622, "lon": -8.658, "gen": "Gen 3",    "adapt": "Trial strip for milling quality with a local baker."},
        ],
        "quantity_kg": 2.5,
        "price": "€8/kg",
        "availability": "After harvest",
        "organic": True,
        "royalty_status": "Open — royalty-free in the Commons",
    },
    "Painted Lady Bean": {
        "crop": "Legume", "sci": "Phaseolus coccineus",
        "note": "A runner bean with bicoloured blossom, grown as much for the bees as the pod. Dry seed is a marbled keeper.",
        "lineage": [
            {"year": 2020, "stage": "Origin",  "place": "Irish Seed Savers Collection", "grower": "Capparoe, Scariff", "county": "Clare",     "lat": 52.910, "lon": -8.529, "gen": "Gen 0", "adapt": "Drawn from the heritage bean collection."},
            {"year": 2022, "stage": "Past",    "place": "Ennis Allotments",             "grower": "Siobhán Murphy",    "county": "Clare",     "lat": 52.845, "lon": -8.987, "gen": "Gen 1", "adapt": "Selected for early, reliable pod set in a short season."},
            {"year": 2024, "stage": "Current", "place": "Cloughjordan Community Farm",  "grower": "Pádraig Flynn",     "county": "Tipperary", "lat": 52.949, "lon": -8.032, "gen": "Gen 2", "adapt": "Grown up willow tripods within the ecovillage gardens."},
            {"year": 2025, "stage": "Current", "place": "Gort Walled Garden",           "grower": "Aoife Kavanagh",    "county": "Galway",    "lat": 53.067, "lon": -8.821, "gen": "Gen 2", "adapt": "Kept as the pollinator strip along the orchard edge."},
        ],
        "quantity_kg": 0.7,
        "price": "Swap only",
        "availability": "After harvest",
        "organic": False,
        "royalty_status": "Open — royalty-free in the Commons",
    },
    "Irish Lovage": {
        "crop": "Herb", "sci": "Levisticum officinale",
        "note": "A towering perennial herb with a celery-and-stock flavour. Seed and root divisions both travel between farms.",
        "lineage": [
            {"year": 2017, "stage": "Origin",  "place": "Old monastery garden",  "grower": "Knowledge of S. Murphy", "county": "Clare",    "lat": 52.840, "lon": -8.992, "gen": "Heirloom", "adapt": "Rescued from an abandoned walled garden."},
            {"year": 2021, "stage": "Past",    "place": "Ennis Allotments",      "grower": "Siobhán Murphy",         "county": "Clare",    "lat": 52.842, "lon": -8.990, "gen": "Gen 1",    "adapt": "Divided and shared at the autumn knowledge swap."},
            {"year": 2024, "stage": "Current", "place": "Newcastle West Garden", "grower": "Máire Ó'Brien",          "county": "Limerick", "lat": 52.449, "lon": -9.061, "gen": "Gen 2",    "adapt": "Seed dried in the shared drying room for redistribution."},
            {"year": 2025, "stage": "Current", "place": "Loughrea Co-op Field",  "grower": "Brigid Ní Fhaoláin",     "county": "Galway",   "lat": 53.200, "lon": -8.564, "gen": "Gen 2",    "adapt": "Now anchoring the perennial herb bed."},
        ],
        "quantity_kg": 0.5,
        "price": "€15/kg",
        "availability": "Available now",
        "organic": True,
        "royalty_status": "Open — royalty-free in the Commons",
    },
    "Purple Sprouting Broccoli": {
        "crop": "Brassica", "sci": "Brassica oleracea",
        "note": "An overwintering brassica that bridges the hungry gap in March — its violet spears are the first fresh crop of the year.",
        "lineage": [
            {"year": 2019, "stage": "Origin",  "place": "Irish Seed Savers Collection", "grower": "Capparoe, Scariff", "county": "Clare",     "lat": 52.909, "lon": -8.530, "gen": "Gen 0", "adapt": "Selected line for late-spring sprouting."},
            {"year": 2022, "stage": "Past",    "place": "Loughrea Co-op Field",         "grower": "Brigid Ní Fhaoláin","county": "Galway",    "lat": 53.199, "lon": -8.565, "gen": "Gen 1", "adapt": "Chosen for hardiness through Atlantic winters."},
            {"year": 2024, "stage": "Past",    "place": "Newcastle West Garden",        "grower": "Máire Ó'Brien",     "county": "Limerick",  "lat": 52.451, "lon": -9.059, "gen": "Gen 2", "adapt": "Later-sprouting strain isolated to extend the harvest."},
            {"year": 2025, "stage": "Current", "place": "Cloughjordan Community Farm",  "grower": "Pádraig Flynn",     "county": "Tipperary", "lat": 52.950, "lon": -8.031, "gen": "Gen 3", "adapt": "Grown for seed under mesh to keep the line true."},
        ],
        "quantity_kg": 1.0,
        "price": "€10/kg",
        "availability": "Available now",
        "organic": False,
        "royalty_status": "Open — royalty-free in the Commons",
    },
    "Tipperary Gold Tomato": {
        "crop": "Fruit", "sci": "Solanum lycopersicum",
        "note": "A golden bush tomato bred for cold polytunnels — low-acid, honey-sweet, quick to ripen before the autumn light fades.",
        "lineage": [
            {"year": 2020, "stage": "Origin",  "place": "Cloughjordan seed circle", "grower": "P. Flynn selection", "county": "Tipperary", "lat": 52.952, "lon": -8.029, "gen": "Gen 0", "adapt": "Stabilised over four seasons from a golden mutant."},
            {"year": 2023, "stage": "Past",    "place": "Nenagh Tillage Plot",      "grower": "Pádraig Flynn",      "county": "Tipperary", "lat": 52.863, "lon": -8.196, "gen": "Gen 3", "adapt": "Earliness fixed for short, cool seasons."},
            {"year": 2025, "stage": "Current", "place": "Raheen Market Garden",     "grower": "Máire Ó'Brien",      "county": "Limerick",  "lat": 52.621, "lon": -8.659, "gen": "Gen 4", "adapt": "Tunnel-grown for market; seed saved from best trusses."},
            {"year": 2025, "stage": "Current", "place": "Gort Walled Garden",       "grower": "Aoife Kavanagh",     "county": "Galway",    "lat": 53.068, "lon": -8.820, "gen": "Gen 4", "adapt": "Offered to new entrants as a starter seed-saving crop."},
        ],
        "quantity_kg": 0.8,
        "price": "Swap only",
        "availability": "After harvest",
        "organic": True,
        "royalty_status": "Open — royalty-free in the Commons",
    },
    "Rooster Potato": {
        "crop": "Root vegetable (tuber)", "sci": "Solanum tuberosum 'Rooster'",
        "note": "Bred in 1990 by Harry Kehoe at Teagasc Oak Park, Carlow, Rooster now accounts for roughly 60% of Irish potato production. Red skin over yellow, floury flesh; grown from certified seed potatoes rather than true seed.",
        "lineage": [
            {"year": 2010, "stage": "Origin",  "place": "Nenagh Tillage Plot",  "grower": "Pádraig Flynn",      "county": "Tipperary", "lat": 52.862, "lon": -8.199, "gen": "Gen 0", "adapt": "Brought in as certified seed and trialled in the tillage rotation."},
            {"year": 2016, "stage": "Past",    "place": "Raheen Market Garden", "grower": "Máire Ó'Brien",      "county": "Limerick",  "lat": 52.621, "lon": -8.659, "gen": "Gen 1", "adapt": "Earthed up on heavy clay for reliable maincrop yields."},
            {"year": 2023, "stage": "Current", "place": "Ennis Allotments",     "grower": "Siobhán Murphy",     "county": "Clare",     "lat": 52.844, "lon": -8.988, "gen": "Gen 2", "adapt": "Saved as seed tubers and shared once breeders' rights lapsed."},
            {"year": 2025, "stage": "Current", "place": "Loughrea Co-op Field", "grower": "Brigid Ní Fhaoláin", "county": "Galway",    "lat": 53.199, "lon": -8.565, "gen": "Gen 3", "adapt": "Co-op block kept for community seed-potato supply."},
        ],
        "quantity_kg": 25.0,
        "price": "€2.50/kg",
        "availability": "Available now",
        "organic": False,
        "royalty_status": "Open — breeders' rights expired 2021, now royalty-free",
    },
}

GROWERS = {
    "Máire Ó'Brien": {
        "county": "Limerick",
        "years_saving": 9,
        "organic_certified": True,
        "bio": "Máire manages a market garden and saves seeds from heavy clay plots every season.",
    },
    "Pádraig Flynn": {
        "county": "Tipperary",
        "years_saving": 12,
        "organic_certified": True,
        "bio": "Pádraig is a tillage grower who keeps landrace grains and garden vegetables in the same rotation.",
    },
    "Aoife Kavanagh": {
        "county": "Galway",
        "years_saving": 7,
        "organic_certified": True,
        "bio": "Aoife tends a walled garden and focuses on heritage varieties for community seed swaps.",
    },
    "Siobhán Murphy": {
        "county": "Clare",
        "years_saving": 10,
        "organic_certified": True,
        "bio": "Siobhán grows in allotments and shares seed and stories with new growers each year.",
    },
    "Brigid Ní Fhaoláin": {
        "county": "Galway",
        "years_saving": 8,
        "organic_certified": False,
        "bio": "Brigid saves heritage grains and herbs from a mixed co-op field near Loughrea.",
    },
}

CURRENT_USER = {
    "name": "Patrick Murphy",
    "county": "Clare",
    "member_since": 2022,
    "fee_paid": True,
    "organic_status": "Certified Organic 2024",
}

# Map seed display names to asset IDs (filenames without extension)
# This ensures the known filenames in assets/crops/ are matched correctly.
_image_id_map = {
    "Autumn King Carrot": "carrot",
    "Wexford Heritage Oat": "oat",
    "Painted Lady Bean": "runner_bean",
    "Irish Lovage": "lovage",
    "Purple Sprouting Broccoli": "purple_sprouting_broccoli",
    "Tipperary Gold Tomato": "tomato",
    "Rooster Potato": "rooster",
}

# Human-readable labels for Creative Commons license short codes
_LICENSE_LABELS = {
    "cc0": "CC0",
    "pdm": "Public Domain",
    "by": "CC BY",
    "by-sa": "CC BY-SA",
    "by-nc": "CC BY-NC",
    "by-nd": "CC BY-ND",
    "by-nc-sa": "CC BY-NC-SA",
    "by-nc-nd": "CC BY-NC-ND",
}

# Attach `image` (path string) and `credit` (markdown "Photo: [author](url) (License)") to each seed
for _name, _data in SEEDS.items():
    asset_id = _image_id_map.get(_name)
    if asset_id:
        img_path = ASSETS_DIR / f"{asset_id}.jpg"
        if img_path.exists():
            _data["image"] = str(img_path)
        else:
            _data["image"] = None

        cred = _credits.get(asset_id, {})
        if cred:
            author = (cred.get("author") or cred.get("creator") or "").strip()
            license_code = (cred.get("license") or "").strip()
            license_label = _LICENSE_LABELS.get(license_code.lower(), license_code.upper())
            url = (cred.get("url") or "").strip()
            # Hyperlink the author (or the word "source" if no author) to the source URL
            label = author or "source"
            who = f"[{label}]({url})" if url else label
            caption = f"Photo: {who}"
            if license_label:
                caption += f" ({license_label})"
            _data["credit"] = caption
        else:
            _data["credit"] = ""
    else:
        _data["image"] = None
        _data["credit"] = ""

PILOT_STATS = {
    "varieties": 247,
    "member_farms": 43,
    "exchanges_logged": 118,
    "counties": 4,
}

STEWARD = "Nuala Sullivan, Irish Seed Savers"

STAGE_COLOR = {
    "Origin": "black",
    "Past": "green",
    "Current": "orange",
}

# Community knowledge cards surfaced on the Knowledge Commons page.
# "variety" matches a SEEDS key (or None for general); "grower" matches a GROWERS key (or None).
KNOWLEDGE = [
    {
        "title": "Saving carrot seed true to type",
        "variety": "Autumn King Carrot", "grower": "Aoife Kavanagh", "county": "Galway",
        "date": "2025-03-12", "type": "Seed-saving",
        "body": "Carrots are biennial, so lift the best roots in autumn, overwinter them frost-free, and replant in spring to flower. Keep at least 800 m from flowering wild carrot (Queen Anne's lace) or cage the umbels, as they cross readily. Save seed only from roots with true colour, shape and a strong central core.",
    },
    {
        "title": "Drying and threshing oats by hand",
        "variety": "Wexford Heritage Oat", "grower": "Pádraig Flynn", "county": "Tipperary",
        "date": "2024-09-02", "type": "Seed-saving",
        "body": "Cut the oats when the straw has turned golden but before the heads shatter, then stook the sheaves to finish drying in the field for a week or two. Thresh by hand by rubbing the heads over a tub, and winnow on a breezy day to separate grain from chaff. Store fully dry in paper sacks, never plastic, to avoid sweating and mould.",
    },
    {
        "title": "Working heavy clay in a wet spring",
        "variety": None, "grower": "Máire Ó'Brien", "county": "Limerick",
        "date": "2025-04-20", "type": "Soil & climate",
        "body": "Heavy estuary clay smears and compacts if you dig or walk on it while it's wet, so wait until a fistful crumbles rather than smears before working it. Permanent raised beds and a winter cover of field beans or rye keep the structure open and let you sow earlier. A thick autumn mulch means the worms do most of next year's digging for you.",
    },
    {
        "title": "Why we keep the Wexford oat",
        "variety": "Wexford Heritage Oat", "grower": None, "county": "Tipperary",
        "date": "2023-11-15", "type": "Heritage story",
        "body": "This tall landrace oat came west with a retiring Wexford tillage farmer who had grown it on the same ground for decades. We keep it not for record yields but because its long straw still thatches and beds animals, and it mills to a porridge with real flavour. Every grower who saves a handful keeps that lineage alive for the next.",
    },
    {
        "title": "Roguing brassicas to keep the line true",
        "variety": "Purple Sprouting Broccoli", "grower": "Brigid Ní Fhaoláin", "county": "Galway",
        "date": "2025-02-01", "type": "Seed-saving",
        "body": "Brassicas are insect-pollinated and cross widely, so isolate your seed plants from other flowering brassicas or net them with a tame pollinator. Through winter, rogue out any plants that bolt early, lack vigour, or sprout the wrong colour before they can flower. Save seed from a block of at least a dozen strong plants to keep the genetic base wide.",
    },
    {
        "title": "Storing seed potatoes through the winter",
        "variety": "Rooster Potato", "grower": "Siobhán Murphy", "county": "Clare",
        "date": "2024-10-10", "type": "Soil & climate",
        "body": "Rooster keeps best as seed when lifted in dry weather and cured for a week somewhere airy before storing. Hold the tubers cool, dark and frost-free over winter, then chit them egg-end-up in trays in good light four to six weeks before planting. In blight country, rogue any soft or rotten tubers early and never save seed from a crop that went down badly.",
    },
]


def list_seeds():
    """Return a list of all seed names."""
    return list(SEEDS.keys())


def get_seed(name):
    """
    Get the full seed record by name.
    
    Args:
        name: The seed name (case-sensitive)
    
    Returns:
        The seed dictionary or None if not found.
    """
    return SEEDS.get(name)


# ---- Seed credits: a non-monetary stewardship value (display model only) -----
_CREDIT_BASE = {
    "Herb": 5, "Brassica": 5, "Root": 6, "Fruit": 6,
    "Legume": 7, "Grain": 8, "Root vegetable (tuber)": 8,  # Rooster
}

SEED_CREDITS_INFO = (
    "Seed credits are a non-monetary stewardship value, not money. A variety's credits = "
    "crop-type base × organic (×1.3) × steward-verified (×1.2) × local adaptation "
    "(× 1 + 0.1 per local generation; Heirloom counts as Gen 2). Credits reward local "
    "adaptation and stewardship — members earn them by depositing quality seed and spend "
    "them receiving others' seed. They are never converted to cash."
)


def _gen_number(gen):
    """Local-generation number: 'Gen 4' -> 4, 'Heirloom' -> 2, else 0."""
    g = str(gen).strip()
    if g.lower().startswith("gen"):
        digits = g[3:].strip()
        return int(digits) if digits.isdigit() else 0
    if g.lower() == "heirloom":
        return 2
    return 0


def seed_credits(seed):
    """Stewardship value = base_by_type × quality multiplier.

    multiplier = 1.0 × (1.3 if organic) × 1.2 (verified — all current seeds) ×
                 (1 + 0.1 × local_generation), where local_generation is the highest
    Gen number in the lineage. Returns a rounded integer.
    """
    if not seed:
        return 0
    base = _CREDIT_BASE.get(seed.get("crop"), 6)
    mult = 1.0
    if seed.get("organic"):
        mult *= 1.3
    mult *= 1.2  # steward-verified: treat all current seeds as verified
    local_gen = max((_gen_number(s.get("gen")) for s in seed.get("lineage", [])), default=0)
    mult *= (1 + 0.1 * local_gen)
    return int(round(base * mult))


def get_grower(name):
    """
    Return the grower profile for the given name.

    Args:
        name: The grower name (case-sensitive)

    Returns:
        The grower dictionary or a safe default if not found.
    """
    return GROWERS.get(name, {
        "county": "Unknown",
        "years_saving": 0,
        "organic_certified": False,
        "bio": "Grower information not available.",
    })


def lineage_df(name):
    """
    Return a pandas DataFrame of a seed's lineage.
    
    Args:
        name: The seed name
    
    Returns:
        DataFrame with columns: year, stage, place, grower, county, lat, lon, gen, adapt
        or an empty DataFrame if seed not found.
    """
    seed = get_seed(name)
    if not seed:
        return pd.DataFrame()
    
    return pd.DataFrame(seed.get("lineage", []))


def all_sites_df():
    """
    Return a pandas DataFrame of every site across all seeds.
    
    Returns:
        DataFrame with columns: seed_name, year, stage, place, grower, county, lat, lon, gen, adapt
    """
    rows = []
    for seed_name, seed_data in SEEDS.items():
        for site in seed_data.get("lineage", []):
            row = {"seed_name": seed_name}
            row.update(site)
            rows.append(row)

    return pd.DataFrame(rows)


def get_knowledge_for(variety=None, grower=None):
    """
    Return knowledge cards filtered by variety and/or grower.

    Args:
        variety: seed name to match against a card's "variety" (None to ignore)
        grower:  grower name to match against a card's "grower" (None to ignore)

    Returns:
        A list of matching knowledge dicts (all cards if no filters given).
    """
    results = []
    for card in KNOWLEDGE:
        if variety is not None and card.get("variety") != variety:
            continue
        if grower is not None and card.get("grower") != grower:
            continue
        results.append(card)
    return results
