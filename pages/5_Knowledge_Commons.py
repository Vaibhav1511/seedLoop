import html
from datetime import date

import streamlit as st
from data import KNOWLEDGE, get_knowledge_for, list_seeds, GROWERS
from ui import render_footer, inject_theme

st.set_page_config(page_title="Knowledge Commons", page_icon=":material/menu_book:", layout="wide")

inject_theme()


def render_card(card):
    """Return one knowledge entry as a single-line flex-column .card HTML string."""
    title = html.escape(card.get("title", ""))
    ctype = html.escape(card.get("type", ""))
    body = html.escape(card.get("body", ""))
    variety = card.get("variety")
    variety_line = (
        f'<div style="color:#5d7a4a;font-size:13px;font-weight:600;margin-bottom:2px;">'
        f'🌱 {html.escape(variety)}</div>'
        if variety else ""
    )
    grower = card.get("grower") or "Community"
    meta_bits = [b for b in [grower, card.get("county") or "", card.get("date") or ""] if b]
    meta = html.escape(" · ".join(meta_bits))
    body_style = (
        "font-size:14px;line-height:1.45;margin:0 0 12px 0;"
        "display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden;"
    )
    return (
        '<div class="card" style="display:flex;flex-direction:column;height:100%;margin:0;">'
        f'<span class="badge">{ctype}</span>'
        f'<h4 style="margin:10px 0 2px 0;">{title}</h4>'
        f'{variety_line}'
        f'<div style="{body_style}">{body}</div>'
        f'<div style="color:#7a7a6a;font-size:12px;margin-top:auto;">{meta}</div>'
        '</div>'
    )


def render_grid(cards):
    """Render all cards as ONE CSS-Grid HTML block so they share the grid and reflow."""
    grid_style = (
        "display:grid;"
        "grid-template-columns:repeat(auto-fill, minmax(300px, 1fr));"
        "gap:12px;"
    )
    cards_html = "".join(render_card(c) for c in cards)
    st.markdown(f'<div style="{grid_style}">{cards_html}</div>', unsafe_allow_html=True)


st.title("Knowledge Commons")
st.markdown(
    "Practical seed-saving and growing knowledge, shared by members and tied to the "
    "varieties and growers of the Commons."
)

st.divider()

# Filters
all_types = sorted({c.get("type") for c in KNOWLEDGE if c.get("type")})
fcol1, fcol2 = st.columns([1, 2])
with fcol1:
    selected_type = st.selectbox("Filter by type", options=["All"] + all_types)
with fcol2:
    q = st.text_input("Search knowledge", value="", placeholder="e.g. carrot, isolation, clay")

filtered = list(KNOWLEDGE)
if selected_type != "All":
    filtered = [c for c in filtered if c.get("type") == selected_type]
if q:
    ql = q.lower()

    def matches(c):
        hay = " ".join(str(c.get(k) or "") for k in ("title", "body", "variety", "grower", "county"))
        return ql in hay.lower()

    filtered = [c for c in filtered if matches(c)]

st.write(f"Showing {len(filtered)} of {len(KNOWLEDGE)} knowledge cards")

if filtered:
    render_grid(filtered)
else:
    st.info("No knowledge cards match your filters yet.")

st.divider()

# Contribute knowledge
st.subheader("Contribute knowledge")
st.caption("Share what you've learned — your card joins the Commons below.")

if "contributions" not in st.session_state:
    st.session_state["contributions"] = []

with st.form("contribute_form", clear_on_submit=True):
    c_title = st.text_input("Title")
    c_type = st.selectbox("Type", options=["Seed-saving", "Soil & climate", "Heritage story"])
    cc1, cc2 = st.columns(2)
    with cc1:
        c_variety = st.selectbox("Variety (optional)", options=["—"] + list_seeds())
    with cc2:
        c_grower = st.selectbox("Grower (optional)", options=["—"] + list(GROWERS.keys()))
    c_body = st.text_area("Knowledge / notes")
    submitted = st.form_submit_button("Add to the Commons")
    if submitted:
        if c_title.strip() and c_body.strip():
            st.session_state["contributions"].append({
                "title": c_title.strip(),
                "type": c_type,
                "variety": None if c_variety == "—" else c_variety,
                "grower": None if c_grower == "—" else c_grower,
                "county": GROWERS.get(c_grower, {}).get("county", "") if c_grower != "—" else "",
                "date": date.today().isoformat(),
                "body": c_body.strip(),
            })
            st.success("Added — thanks for sharing!")
        else:
            st.warning("Please add at least a title and some notes.")

contribs = st.session_state["contributions"]
if contribs:
    st.markdown("#### Community contributions")
    render_grid(list(reversed(contribs)))
else:
    st.caption("No community contributions yet — be the first to add one.")

render_footer()
