import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import html
import re
from data import SEEDS, list_seeds, get_seed, lineage_df, all_sites_df, get_knowledge_for, seed_credits
from ui import render_footer, inject_theme

st.set_page_config(page_title="Browse Registry", page_icon=":material/search:", layout="wide")

inject_theme()

# Uniform card height so rows align (backstop; cards are also fixed-height by content)
st.markdown(
    """
    <style>
    div[data-testid="stVerticalBlockBorderWrapper"] { min-height: 480px; }
    </style>
    """,
    unsafe_allow_html=True,
)

CARD_IMG_HEIGHT = 190


def _img_data_uri(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    suffix = path.suffix.lower().lstrip(".")
    mime = "jpeg" if suffix in ("jpg", "jpeg") else (suffix or "jpeg")
    return f"data:image/{mime};base64,{data}"


def card_media_html(seed, name):
    """Fixed-height image (object-fit:cover) or a sage placeholder tile of the same height."""
    img_path = seed.get("image") if seed else None
    if img_path and Path(img_path).exists():
        uri = _img_data_uri(Path(img_path))
        return (
            f'<img src="{uri}" alt="{html.escape(name)}" '
            f'style="width:100%;height:{CARD_IMG_HEIGHT}px;object-fit:cover;'
            f'border-radius:8px;display:block;" />'
        )
    # No image yet (e.g. Rooster): sage placeholder, same height, with the crop name
    crop = html.escape(seed.get("crop", "") if seed else "")
    return (
        f'<div style="width:100%;height:{CARD_IMG_HEIGHT}px;border-radius:8px;'
        f'background-color:#5d7a4a;color:#f4f1e4;display:flex;flex-direction:column;'
        f'align-items:center;justify-content:center;text-align:center;padding:8px;box-sizing:border-box;">'
        f'<div style="font-size:30px;line-height:1;margin-bottom:6px;">🌱</div>'
        f'<div style="font-weight:700;font-size:15px;">{html.escape(name)}</div>'
        f'<div style="font-size:12px;opacity:0.85;">{crop}</div>'
        f'</div>'
    )


def card_text_html(seed, name):
    """Essentials: variety name (clamped to 2 lines, fixed height), crop type, royalty badge."""
    crop = html.escape(seed.get("crop", "") if seed else "")
    royalty = seed.get("royalty_status", "") if seed else ""
    if royalty:
        cls = "badge" if royalty.startswith("Open") else "badge protected"
        badge = f'<span class="{cls}">{html.escape(royalty)}</span>'
    else:
        badge = ""
    return (
        f'<div style="font-weight:700;font-size:1.05rem;line-height:1.25;min-height:2.6em;'
        f'display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;'
        f'margin-bottom:2px;">{html.escape(name)}</div>'
        f'<div style="color:#7a7a6a;font-size:13px;margin-bottom:8px;">{crop}</div>'
        f'<div style="margin-bottom:8px;">{badge}</div>'
    )

# Sidebar filters
st.sidebar.header("Filter the registry")

# Build crop types from SEEDS
_crop_types = sorted({v.get("crop") for v in SEEDS.values() if v.get("crop")})
# Build counties from current sites
_all_sites = all_sites_df()
_current_sites = _all_sites[_all_sites["stage"] == "Current"]
_counties = sorted(_current_sites["county"].dropna().unique().tolist())

selected_crops = st.sidebar.multiselect("Crop type", options=_crop_types, default=_crop_types)
selected_counties = st.sidebar.multiselect("County (current growth)", options=_counties, default=_counties)

# Search box
q = st.sidebar.text_input("Search by name", value="")

# Prepare seed list and apply filters
seed_names = list_seeds()

def seed_matches(seed_name: str) -> bool:
    seed = get_seed(seed_name)
    if not seed:
        return False
    # crop filter
    if selected_crops and seed.get("crop") not in selected_crops:
        return False
    # county filter: check if any current-stage county for this seed intersects
    lineage = seed.get("lineage", [])
    current_counties = {s.get("county") for s in lineage if s.get("stage") == "Current"}
    if selected_counties and not (current_counties & set(selected_counties)):
        return False
    # search
    if q:
        qlow = q.lower()
        if qlow not in seed_name.lower() and qlow not in (seed.get("sci") or "").lower() and qlow not in (seed.get("note") or "").lower():
            return False
    return True

filtered = [name for name in seed_names if seed_matches(name)]

st.title("Browse the Seed Registry")
st.write(f"Showing {len(filtered)} of {len(seed_names)} varieties")

# Layout: light cards in rows of 3 (real columns/containers/buttons — buttons stay interactive)
cols_per_row = 3
cols = st.columns(cols_per_row)
for i, name in enumerate(filtered):
    col = cols[i % cols_per_row]
    with col:
        seed = get_seed(name)
        with st.container(border=True):
            st.markdown(card_media_html(seed, name), unsafe_allow_html=True)
            # Single-line muted credit so every card is the same height (full clickable
            # credit is shown in the detail view). Strip the markdown link to plain text.
            credit = seed.get("credit", "") if seed else ""
            credit_text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", credit) if credit else "Photo coming soon"
            st.markdown(
                f'<div style="color:#7a7a6a;font-size:12px;white-space:nowrap;overflow:hidden;'
                f'text-overflow:ellipsis;margin:2px 0 6px 0;">{html.escape(credit_text)}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(card_text_html(seed, name), unsafe_allow_html=True)

            if st.button("View details", key=f"detail_{name}", use_container_width=True):
                st.session_state['selected_seed'] = name
                st.session_state['view'] = 'detail'
            if st.button("Trace this seed → Seed Atlas", key=f"trace_{name}", use_container_width=True):
                st.session_state['selected_seed'] = name
                st.session_state['view'] = 'trace'
                st.info("Seed selected for tracing. Open the Seed Atlas page to view its provenance.")

# If session has selected seed and view=detail, render detail below
if st.session_state.get('selected_seed') and st.session_state.get('view') == 'detail':
    sel = st.session_state['selected_seed']
    st.divider()
    st.header(f"Details — {sel}")
    seed = get_seed(sel)
    # Essentials moved off the light cards
    st.markdown(f"*{seed.get('sci','')}*")
    st.markdown(f"**Crop:** {seed.get('crop','')}")
    _lineage = seed.get("lineage", [])
    _current = [s for s in _lineage if s.get("stage") == "Current"]
    _counties = sorted({s.get("county") for s in _current})
    _gens = sorted({s.get("gen") for s in _current})
    st.markdown(f"**Currently grown in:** {', '.join(_counties) if _counties else '—'}")
    st.markdown(f"**Local generation:** {', '.join(_gens) if _gens else '—'}")
    royalty = seed.get("royalty_status", "")
    if royalty:
        cls = "badge" if royalty.startswith("Open") else "badge protected"
        st.markdown(f'<span class="{cls}">{royalty}</span>', unsafe_allow_html=True)
    credit = seed.get("credit", "")
    if credit:
        st.caption(credit)
    _credits = seed_credits(seed)
    st.markdown(
        f'<div class="card" style="padding:14px 16px;">'
        f'<span class="badge">{_credits} credits</span>'
        f'<div style="margin-top:8px;font-size:0.9rem;color:#5B5345;">'
        f'<strong>Stewardship value: {_credits} credits.</strong> Credits — not money — are '
        f'how members exchange, rewarding local adaptation and stewardship.</div></div>',
        unsafe_allow_html=True,
    )
    st.subheader("Full note")
    st.write(seed.get('note',''))
    st.subheader("Traits & Lineage")
    df = lineage_df(sel)
    if not df.empty:
        st.dataframe(df.sort_values(['year']))
    else:
        st.write("No lineage data available.")

    st.subheader("Knowledge about this variety")
    notes = get_knowledge_for(variety=sel)
    if notes:
        for k in notes:
            title = html.escape(k.get("title", ""))
            grower = html.escape(k.get("grower") or "Community")
            body = html.escape(k.get("body", ""))
            st.markdown(
                f'<div class="card">'
                f'<div style="font-weight:700;font-size:1rem;margin-bottom:2px;">{title}</div>'
                f'<div style="color:#7a7a6a;font-size:13px;margin-bottom:6px;">{grower}</div>'
                f'<div style="font-size:14px;line-height:1.45;display:-webkit-box;'
                f'-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">{body}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.caption("No knowledge notes yet — add one in Knowledge Commons.")
        st.page_link("pages/5_Knowledge_Commons.py", label="Open Knowledge Commons", icon=":material/menu_book:")

render_footer()
