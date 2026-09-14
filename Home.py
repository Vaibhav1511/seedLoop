import base64
import html
from pathlib import Path

import streamlit as st
from data import PILOT_STATS, list_seeds, get_seed
from ui import _logo_icon_b64, render_footer, inject_theme, render_sidebar

# Page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="SeedLoop",
    page_icon=":material/eco:",
    layout="wide",
)

# Inject theme + the sidebar brand block on every page load
inject_theme()
render_sidebar()

# Hero — photo with a left-to-right moss gradient; eyebrow + headline + subcopy on top.
# Falls back to a solid moss banner if the photo is missing so the page never breaks.
# The logo lives inside the hero itself now (top-left badge: a small full-colour
# medallion + the wordmark as real text) instead of floating alone above it.
_hero = Path(__file__).parent / "assets" / "hero.jpg"
if _hero.exists():
    _hero_b64 = base64.b64encode(_hero.read_bytes()).decode("ascii")
    _photo = f", url('data:image/jpeg;base64,{_hero_b64}') center/cover no-repeat"
else:
    _photo = ""

_logo = _logo_icon_b64()
_logo_badge = (
    f'<div class="hero-logo">'
    f'<div class="logo-medallion"><img src="data:image/png;base64,{_logo}" alt="" /></div>'
    f'<div class="wordmark">SeedLoop</div>'
    f'</div>'
    if _logo else ""
)

st.markdown(
    f'<div style="position:relative;border-radius:18px;overflow:hidden;padding:72px 56px 64px;'
    f'margin:0 0 24px 0;background:linear-gradient(105deg, rgba(35,52,30,.88) 0%, '
    f'rgba(35,52,30,.55) 55%, rgba(35,52,30,.15) 100%){_photo}, #2E4A2C;">'
    f'{_logo_badge}'
    f'<span class="eyebrow">Farmer-owned · Member-governed</span>'
    f'<h1 style="color:#F7F5EC;font-size:clamp(2.4rem,5vw,3.6rem);line-height:1.05;'
    f'max-width:14ch;margin:22px 0 16px;">Every seed has a '
    f'<em style="font-style:italic;color:#C9A24B;">story worth tracing.</em></h1>'
    f'<p style="color:#E4E2D2;font-size:1.08rem;line-height:1.6;max-width:46ch;margin:0;">'
    f'SeedLoop is the open registry and traceability commons for the Irish Midwest. '
    f'Forty-three farms keep heritage varieties moving from hand to hand — '
    f'governed by members, not corporations.</p></div>',
    unsafe_allow_html=True,
)

# Hero CTAs — real Streamlit buttons (navigation can't live in the hero HTML).
# Primary → barley; secondary → outlined moss (from ui.py).
st.markdown(
    """<style>
    .stButton > button[data-testid="stBaseButton-primary"]{
        background-color:#C9A24B; color:#2A2113; box-shadow:0 6px 18px rgba(0,0,0,.20); }
    .stButton > button[data-testid="stBaseButton-primary"]:hover{
        background-color:#b8902f; color:#2A2113; }
    </style>""",
    unsafe_allow_html=True,
)
_l, _cta_browse, _cta_trace, _r = st.columns([3, 2, 2, 3])
with _cta_browse:
    if st.button("Browse the registry", type="primary", use_container_width=True):
        st.switch_page("pages/1_Browse_Registry.py")
with _cta_trace:
    if st.button("Trace a seed", type="secondary", use_container_width=True):
        st.switch_page("pages/2_Seed_Atlas.py")

# Field-strip stat band — farm parcels seen from the air, fed by PILOT_STATS.
st.markdown(
    f'<div class="strips">'
    f'<div class="strip"><div class="num">{PILOT_STATS["varieties"]}</div><div class="lbl">Seed varieties</div></div>'
    f'<div class="strip"><div class="num">{PILOT_STATS["member_farms"]}</div><div class="lbl">Member farms</div></div>'
    f'<div class="strip"><div class="num">{PILOT_STATS["exchanges_logged"]}</div><div class="lbl">Exchanges logged</div></div>'
    f'<div class="strip"><div class="num">{PILOT_STATS["counties"]}</div><div class="lbl">Counties</div></div>'
    f'</div>',
    unsafe_allow_html=True,
)

# How the commons works — the SeedLoop cycle (List → Exchange → Grow → Return)
st.markdown('<div class="section-head"><h2>How the commons works</h2><span class="tick"></span></div>',
            unsafe_allow_html=True)
st.caption("A seed makes one full loop through the commons — and comes back to local soil.")
_loop = [
    ("1", "List a seed", "Record a variety with its lineage, growing notes and the farm it comes from. Listing takes about five minutes."),
    ("2", "Exchange", "Members request seed directly. Every handover is logged, so a variety's provenance is never lost."),
    ("3", "Grow & observe", "Growers add field notes each season — germination, hardiness, flavour — building shared knowledge."),
    ("4", "Return seed", "Saved seed flows back into the registry, closing the loop and keeping varieties alive in local soil."),
]
for _i, (_col, (_n, _title, _body)) in enumerate(zip(st.columns(4, gap="medium"), _loop)):
    with _col:
        st.markdown(
            f'<div class="loop-card{" closing" if _i == 3 else ""}">'
            f'<div class="step">{_n}</div><h3>{html.escape(_title)}</h3>'
            f'<p>{html.escape(_body)}</p></div>', unsafe_allow_html=True,
        )

# From the registry — live preview of three varieties pulled from data.py
st.markdown('<div class="section-head"><h2>From the registry</h2><span class="tick"></span></div>',
            unsafe_allow_html=True)
st.caption("A few varieties members are keeping alive right now.")
_SWATCH = {"Root": "#C9A24B", "Grain": "#B5894A", "Legume": "#4F7A45", "Herb": "#6E8B3D",
           "Brassica": "#6B4E8E", "Fruit": "#B23A48", "Tuber": "#8A6D3B"}


def _current_county(seed):
    cur = [s.get("county") for s in seed.get("lineage", []) if s.get("stage") == "Current"]
    return cur[0] if cur else (seed.get("lineage") or [{}])[-1].get("county", "—")


for _col, _name in zip(st.columns(3, gap="medium"), list_seeds()[:3]):
    _seed = get_seed(_name)
    _crop = _seed.get("crop", "")
    _royalty = _seed.get("royalty_status", "")
    _meta = "Open · royalty-free" if _royalty.startswith("Open") else "Royalty-bearing variety"
    with _col:
        st.markdown(
            f'<div class="seed-card"><div class="swatch" style="background:{_SWATCH.get(_crop, "#7A9A57")};"></div>'
            f'<div class="pad"><div class="county">Co. {html.escape(_current_county(_seed))} · {html.escape(_crop)}</div>'
            f'<h4>{html.escape(_name)}</h4>'
            f'<p style="display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;">'
            f'{html.escape(_seed.get("note", ""))}</p>'
            f'<div class="meta">{html.escape(_meta)}</div></div></div>', unsafe_allow_html=True,
        )

st.page_link("pages/1_Browse_Registry.py",
             label=f"See all {PILOT_STATS['varieties']} varieties", icon=":material/arrow_forward:")

# Member voice — moss quote band (sample testimonial, Co. Limerick grower)
st.markdown(
    '<div class="quote"><blockquote>“A variety my grandmother kept going isn’t mine to lose — '
    'through the registry it belongs to all of us.”</blockquote>'
    '<cite>Máire Ó’Brien · Member farm, Co. Limerick</cite></div>',
    unsafe_allow_html=True,
)

render_footer()
