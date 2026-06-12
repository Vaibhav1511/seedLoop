import html

import streamlit as st
import folium
from streamlit_folium import st_folium
from folium import CircleMarker, Popup, PolyLine
from branca.colormap import linear
from data import SEEDS, list_seeds, get_seed, all_sites_df, STEWARD
from ui import inject_theme

st.set_page_config(page_title="Seed Atlas", page_icon=":material/map:", layout="wide")

inject_theme()

# ---------------------------------------------------------------- page-local styling
st.markdown("""
<style>
/* panel labels in the sidebar */
.panel-label{ font-size:.66rem; text-transform:uppercase; letter-spacing:.16em;
              color:#BFCBA8; font-weight:600; margin:12px 0 6px; }
/* view selector → segmented control */
section[data-testid="stSidebar"] div[role="radiogroup"]{
    display:flex; background:rgba(247,245,236,.10); border-radius:9px; padding:3px;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label{
    flex:1; display:flex; justify-content:center; align-items:center;
    margin:0 !important; padding:7px 6px !important; border-radius:7px; cursor:pointer;
    transition:background .15s ease;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child{ display:none !important; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label p{
    color:#D9D6C2 !important; font-size:.82rem !important; font-weight:600 !important; margin:0 !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked){ background:#F7F5EC; }
section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p{ color:var(--moss) !important; }
/* selectbox */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div{
    background:#FFFEF7 !important; border-radius:9px !important; border:1px solid #E3DFC9 !important;
}
section[data-testid="stSidebar"] div[data-baseweb="select"] *{ color:var(--peat) !important; }
section[data-testid="stSidebar"] div[data-baseweb="select"] svg{ fill:var(--peat) !important; }
/* toggle / checkbox → barley when on; cream 0.8rem label */
section[data-testid="stSidebar"] [data-baseweb="checkbox"] [aria-checked="true"]{
    background:var(--barley) !important; border-color:var(--barley) !important;
}
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p{ color:#D9D6C2 !important; font-size:.8rem !important; }
.sidebar-divider2{ border:none; border-top:1px solid rgba(247,245,236,.22); margin:14px 0 6px; }
/* leaf eyebrow + gen pill + meta */
.atlas-eyebrow{ font-size:.68rem; text-transform:uppercase; letter-spacing:.2em; color:var(--leaf); font-weight:600; }
.gen-pill{ background:var(--barley); color:#2A2113; font-size:.72rem; font-weight:700;
           letter-spacing:.07em; padding:5px 12px; border-radius:999px; white-space:nowrap; }
.atlas-meta{ font-size:.85rem; color:#8A8268; margin:4px 0 18px; }
/* commons ownership band */
.commons-band{ background:var(--field); border-left:4px solid var(--barley); border-radius:10px;
               padding:16px 20px; margin:0 0 18px; display:flex; align-items:center; gap:12px; }
.commons-band .glyph{ color:var(--moss); font-size:1.4rem; line-height:1; }
.commons-band .txt{ font-family:'Fraunces',serif; font-style:italic; font-size:1rem; color:#4A4234; }
/* map card header bar */
.map-head{ background:#FFFEF7; border:1px solid #E3DFC9; border-bottom:none;
           border-radius:14px 14px 0 0; padding:13px 18px; display:flex;
           justify-content:space-between; align-items:center; }
.map-head .lbl{ font-size:.68rem; text-transform:uppercase; letter-spacing:.1em; color:#8A8268; }
.map-head .legend{ font-size:.66rem; background:#EFEDDD; border:1px solid #DCD7BD;
                   border-radius:999px; padding:3px 10px; color:#5B5345; }
iframe[title^="streamlit_folium"]{ border:1px solid #E3DFC9 !important; border-top:none !important;
                                   border-radius:0 0 14px 14px !important; }
/* mini stat strips (right column) */
.mini-strip{ border-radius:12px; padding:16px 18px; margin-bottom:10px; }
.mini-strip .n{ font-family:'Fraunces',serif; font-size:1.9rem; font-weight:600; line-height:1; }
.mini-strip .l{ font-size:.64rem; text-transform:uppercase; letter-spacing:.12em; margin-top:6px; opacity:.85; }
/* provenance timeline */
.tl{ position:relative; padding-left:34px; margin-top:18px; }
.tl .spine{ position:absolute; left:9px; top:6px; bottom:6px; border-left:2px dashed #C9C4AC; }
.tl .entry{ position:relative; margin-bottom:30px; }
.tl .node{ position:absolute; left:-34px; top:0; width:20px; height:20px; border-radius:50%;
           font-family:'Fraunces',serif; font-weight:700; font-size:.62rem;
           display:flex; align-items:center; justify-content:center; }
.tl .yr{ font-size:.68rem; letter-spacing:.16em; color:var(--barley); font-weight:600; text-transform:uppercase; }
.tl .place{ font-family:'Fraunces',serif; font-weight:600; font-size:1.15rem; color:var(--peat); margin:2px 0; }
.tl .grower{ font-size:.8rem; color:var(--leaf); margin-bottom:4px; }
.tl .grower b{ font-weight:600; }
.tl .note{ font-size:.86rem; color:#5B5345; max-width:52ch; }
/* footer row */
.atlas-foot{ display:flex; justify-content:space-between; border-top:1px solid #E3DFC9;
             padding-top:18px; margin-top:30px; font-size:.78rem; }
.atlas-foot .l{ color:var(--moss); font-weight:500; }
.atlas-foot .r{ color:#8A8268; }
@media (max-width:900px){ .map-head .legend{ display:none; } }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------- sidebar controls
st.sidebar.markdown('<div class="panel-label">Map view</div>', unsafe_allow_html=True)
view = st.sidebar.radio("View", ["Single seed", "Whole Commons"], horizontal=True, label_visibility="collapsed")

st.sidebar.markdown('<div class="panel-label">Select seed</div>', unsafe_allow_html=True)
_seeds = list_seeds()
seed_default = st.session_state.get("selected_seed") or (_seeds[0] if _seeds else None)
sel_seed = st.sidebar.selectbox(
    "Select seed", options=_seeds,
    index=(_seeds.index(seed_default) if seed_default in _seeds else 0),
    label_visibility="collapsed",
)
show_line = st.sidebar.toggle("Show chronological route", value=True)
st.sidebar.markdown('<hr class="sidebar-divider2">', unsafe_allow_html=True)

all_sites = all_sites_df()


def _gennum(g):
    g = str(g)
    return g.replace("Gen", "").strip() if g.lower().startswith("gen") else (g[:1] or "•")


# ================================================================ SINGLE SEED VIEW
if view == "Single seed":
    seed_name = sel_seed
    seed = get_seed(seed_name)
    lin = sorted(seed.get("lineage", []), key=lambda r: r.get("year", 0))

    if not lin:
        st.markdown(f'<div class="atlas-eyebrow">Seed Atlas · Provenance &amp; Maps</div>', unsafe_allow_html=True)
        st.markdown(f"<h1>{html.escape(seed_name)}</h1>", unsafe_allow_html=True)
        st.write("No lineage data available for this seed.")
        st.stop()

    first_year = lin[0].get("year", "—")
    last_year = lin[-1].get("year", "—")
    current = [r for r in lin if r.get("stage") == "Current"]
    cur_gen = (current[-1] if current else lin[-1]).get("gen", "—")
    grow_sites = len(lin)
    counties_n = len({r.get("county") for r in lin})
    farms_now = len({r.get("grower") for r in current})

    if str(cur_gen).lower().startswith("gen"):
        pill = f"GEN {_gennum(cur_gen)} · ACTIVE"
    else:
        pill = f"{str(cur_gen).upper()} · ACTIVE"

    # ---- header
    st.markdown('<div class="atlas-eyebrow">Seed Atlas · Provenance &amp; Maps</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:14px;flex-wrap:wrap;">'
        f'<h1 style="font-size:2.5rem;font-weight:700;margin:6px 0;">{html.escape(seed_name)}</h1>'
        f'<span class="gen-pill">{pill}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="atlas-meta">{html.escape(seed.get("sci",""))} · '
        f'entered the commons {first_year} · steward {html.escape(STEWARD)}</div>',
        unsafe_allow_html=True,
    )

    # ---- commons ownership band (replaces st.info)
    st.markdown(
        '<div class="commons-band"><span class="glyph">↺</span>'
        '<span class="txt">This provenance record is owned by the Commons — '
        'it cannot be enclosed or royalty-charged.</span></div>',
        unsafe_allow_html=True,
    )

    # ---- map + stats
    map_col, info_col = st.columns([3, 1])
    with map_col:
        st.markdown(
            f'<div class="map-head"><span class="lbl">Journey across the Midwest · {first_year} – {last_year}</span>'
            f'<span class="legend">– – Chronological route</span></div>',
            unsafe_allow_html=True,
        )
        m = folium.Map(location=[52.85, -8.55], zoom_start=8, tiles="CartoDB positron")
        points = []
        for r in lin:
            lat, lon = r.get("lat"), r.get("lon")
            is_cur = r.get("stage") == "Current"
            bg = "#C9A24B" if is_cur else "#FFFFFF"
            bd = "#C9A24B" if is_cur else "#2E4A2C"
            tx = "#2A2113" if is_cur else "#2E4A2C"
            popup_html = (
                f"<b>{html.escape(str(r.get('place')))}</b><br>Grower: {html.escape(str(r.get('grower')))}"
                f"<br>County: {html.escape(str(r.get('county')))}<br>Year: {r.get('year')} · {r.get('gen')}"
                f"<br>{html.escape(str(r.get('adapt')))}"
            )
            node = (
                f'<div style="width:22px;height:22px;border-radius:50%;background:{bg};'
                f'border:2.5px solid {bd};color:{tx};font-family:Fraunces,serif;font-weight:700;'
                f'font-size:11px;display:flex;align-items:center;justify-content:center;'
                f'box-shadow:0 1px 3px rgba(0,0,0,.3);">{_gennum(r.get("gen"))}</div>'
            )
            folium.Marker(
                location=(lat, lon),
                icon=folium.DivIcon(html=node, icon_size=(22, 22), icon_anchor=(11, 11)),
                popup=Popup(popup_html, max_width=300),
            ).add_to(m)
            points.append((lat, lon))
        if show_line and len(points) > 1:
            PolyLine(points, color="#3A2F25", weight=2, opacity=0.65, dash_array="7,6").add_to(m)
        st_folium(m, width="100%", height=560)

    with info_col:
        strips = [
            (str(grow_sites), "Grow sites", "#33502F", "#F1EFDF"),
            (str(counties_n), "Counties", "#4F7A45", "#F1EFDF"),
            (str(farms_now), "Farms now growing", "#7A9A57", "#23341E"),
            (str(cur_gen), "Current generation", "#C9A24B", "#2A2113"),
        ]
        strips_html = "".join(
            f'<div class="mini-strip" style="background:{bg};color:{fg};">'
            f'<div class="n">{html.escape(val)}</div><div class="l">{label}</div></div>'
            for val, label, bg, fg in strips
        )
        st.markdown(strips_html, unsafe_allow_html=True)

    # ---- provenance timeline
    st.markdown('<div class="section-head"><h2 style="font-size:1.7rem;">Provenance timeline</h2>'
                '<span class="tick"></span></div>', unsafe_allow_html=True)
    tl = '<div class="tl"><div class="spine"></div>'
    for r in lin:
        is_cur = r.get("stage") == "Current"
        nbg = "#C9A24B" if is_cur else "#FFFFFF"
        nbd = "#C9A24B" if is_cur else "#2E4A2C"
        ntx = "#2A2113" if is_cur else "#2E4A2C"
        tl += (
            '<div class="entry">'
            f'<div class="node" style="background:{nbg};border:2.5px solid {nbd};color:{ntx};">{_gennum(r.get("gen"))}</div>'
            f'<div class="yr">{r.get("year")} · {html.escape(str(r.get("gen")))}</div>'
            f'<div class="place">{html.escape(str(r.get("place")))}</div>'
            f'<div class="grower">GROWER <b>{html.escape(str(r.get("grower")))}</b> · Co. {html.escape(str(r.get("county")))}</div>'
            f'<div class="note">{html.escape(str(r.get("adapt")))}</div>'
            '</div>'
        )
    tl += '</div>'
    st.markdown(tl, unsafe_allow_html=True)

# ================================================================ WHOLE COMMONS VIEW
elif view == "Whole Commons":
    st.markdown('<div class="atlas-eyebrow">Seed Atlas · Provenance &amp; Maps</div>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size:2.5rem;font-weight:700;margin:6px 0 14px;">All sites across the Commons</h1>',
                unsafe_allow_html=True)

    crop_types = sorted({v.get('crop') for v in SEEDS.values() if v.get('crop')})
    counties = sorted(all_sites['county'].dropna().unique().tolist())
    st.sidebar.markdown('<div class="panel-label">Filter</div>', unsafe_allow_html=True)
    sel_crops = st.sidebar.multiselect("Crop", options=crop_types, default=crop_types)
    sel_counties = st.sidebar.multiselect("County", options=counties, default=counties)

    df = all_sites.copy()
    if sel_crops:
        valid_seeds = [name for name, s in SEEDS.items() if s.get('crop') in sel_crops]
        df = df[df['seed_name'].isin(valid_seeds)]
    if sel_counties:
        df = df[df['county'].isin(sel_counties)]

    if df.empty:
        st.write("No sites match the selected filters.")
    else:
        seeds = df['seed_name'].unique().tolist()
        cmap = linear.Set1_09.scale(0, max(1, len(seeds)))
        seed_colors = {s: cmap(i % 9) for i, s in enumerate(seeds)}

        st.markdown('<div class="map-head"><span class="lbl">All grow sites across the Commons</span></div>',
                    unsafe_allow_html=True)
        m = folium.Map(location=[52.85, -8.55], zoom_start=8, tiles="CartoDB positron")
        for _, row in df.iterrows():
            color = seed_colors.get(row.get('seed_name'), '#3388ff')
            popup_html = (
                f"<b>{html.escape(str(row.get('seed_name')))}</b><br>Place: {html.escape(str(row.get('place')))}"
                f"<br>Grower: {html.escape(str(row.get('grower')))}<br>County: {html.escape(str(row.get('county')))}"
                f"<br>Year: {row.get('year')} · {row.get('gen')}"
            )
            CircleMarker(location=(row.get('lat'), row.get('lon')), radius=6, color="#2E4A2C", weight=2,
                         fill=True, fill_color=color, fill_opacity=0.9,
                         popup=Popup(popup_html, max_width=300)).add_to(m)

        legend = ('<div style="position:fixed;bottom:50px;left:10px;z-index:9999;background:#FFFEF7;'
                  'padding:12px 14px;border:1px solid #E3DFC9;border-radius:12px;'
                  'box-shadow:0 2px 10px rgba(58,47,37,.12);max-height:300px;overflow:auto;'
                  "font-family:'Public Sans',sans-serif;color:#3A2F25;font-size:.8rem;\">"
                  '<div style="font-weight:600;margin-bottom:6px;">Seed legend</div>')
        for s, c in seed_colors.items():
            legend += (f"<div style='margin:2px 0;'><i style='background:{c};width:11px;height:11px;"
                       f"display:inline-block;border-radius:50%;margin-right:8px;'></i>{html.escape(str(s))}</div>")
        legend += "</div>"
        m.get_root().html.add_child(folium.Element(legend))
        st_folium(m, width="100%", height=640)

    st.markdown('<div class="section-head"><h2 style="font-size:1.7rem;">Commons at a glance</h2>'
                '<span class="tick"></span></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Sites by county**")
        st.bar_chart(all_sites['county'].value_counts())
    with col2:
        st.markdown("**Sites by stage**")
        st.bar_chart(all_sites['stage'].value_counts())

# ---------------------------------------------------------------- footer row
st.markdown(
    f'<div class="atlas-foot"><span class="l">🌱 Governed by members, not corporations</span>'
    f'<span class="r">Steward: {html.escape(STEWARD)}</span></div>',
    unsafe_allow_html=True,
)
