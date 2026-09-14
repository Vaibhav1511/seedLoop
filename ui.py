import base64
from pathlib import Path

import streamlit as st
from data import STEWARD


@st.cache_data
def _logo_icon_b64():
    """Base64 of the full-colour SeedLoop icon (cropped from the lockup, wordmark
    excluded). Sits inside a small parchment medallion on dark surfaces (moss
    sidebar, hero photo) — the wordmark itself is set as real HTML text alongside
    it, rather than baked into a raster image, so it stays crisp at any size."""
    logo_path = Path(__file__).parent / "assets" / "logo-icon.png"
    return base64.b64encode(logo_path.read_bytes()).decode("ascii") if logo_path.exists() else None


def inject_theme():
    """
    Inject the shared SeedLoop theme — moss + barley + parchment, Fraunces + Public Sans.
    Call this at the top of every page. See DESIGN.md for the full system.
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;0,9..144,700;1,9..144,400&family=Public+Sans:wght@400;500;600&display=swap');

    :root{
        --moss:      #2E4A2C;   /* deep hedgerow green */
        --leaf:      #4F7A45;   /* mid leaf green */
        --barley:    #C9A24B;   /* ripe barley gold */
        --peat:      #3A2F25;   /* peat-brown ink */
        --parchment: #F7F5EC;   /* paper background */
        --field:     #EDEADB;   /* pale field strip */
        --card:      #FFFEF7;   /* card surface */
        --card-bd:   #E3DFC9;   /* card border */
    }

    /* ---- global canvas --------------------------------------------------- */
    html, body, [class*="stApp"]{
        background-color: var(--parchment);
        color: var(--peat);
        font-family: 'Public Sans', sans-serif;
    }
    [data-testid="stToolbar"]{ display:none; }
    #MainMenu{ visibility:hidden; }
    footer{ visibility:hidden; }
    /* header kept transparent (not removed) so the sidebar toggle still works */
    header[data-testid="stHeader"]{ background:transparent; }
    .block-container{ padding-top:1.4rem; max-width:1080px; }

    /* ---- typography ------------------------------------------------------ */
    h1,h2,h3,h4{ font-family:'Fraunces', serif; color:var(--peat); font-weight:600; }
    h1{ font-weight:700; }

    /* ---- sidebar (moss) -------------------------------------------------- */
    section[data-testid="stSidebar"]{ background:var(--moss); border-right:none; }
    /* stack the sidebar so the brand block sits ABOVE the native nav */
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"]{ display:flex; flex-direction:column; }
    [data-testid="stSidebarHeader"]{ order:0; }
    [data-testid="stSidebarUserContent"]{ order:1; }
    [data-testid="stSidebarNav"]{ order:2; }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] *,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
    section[data-testid="stSidebar"] label{ color:#E8E6D5 !important; }
    /* native multipage nav — NOTE: stSidebarNav is a <div>, NOT a <section>, so the
       selector must be scoped via the stSidebar <section> and NOT prefixed with
       `section` on the nav testid. Force all nav text/icons white for legibility. */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] *{ color:#FFFFFF !important; }
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]{
        padding:9px 12px !important; border-radius:8px; margin:0 0 2px 0;
        font-size:.98rem !important; transition:background .15s ease;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover{
        background:rgba(247,245,236,.08);
    }
    /* selected item — subtle pill (text already white above) */
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"]{
        background:rgba(247,245,236,.14) !important; font-weight:600;
    }
    /* keep typed input text dark/legible against the pale field-fill inputs */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea{ color:var(--peat) !important; }
    /* full-colour icon in a small circular parchment medallion — a seal/emblem,
       not a card — so its own linework and colour stay intact; the wordmark is
       real text beside it (crisp at any size, unlike the old baked-in raster type). */
    .logo-medallion{ width:96px; height:96px; border-radius:50%; background:var(--parchment);
                      display:flex; align-items:center; justify-content:center; flex-shrink:0;
                      box-shadow:0 4px 14px rgba(0,0,0,.18); margin:0 auto; }
    .logo-medallion img{ width:76px; height:auto; display:block; }
    .sidebar-logo{ margin:4px 0 18px; text-align:center; }
    .sidebar-logo .wordmark{ font-family:'Fraunces',serif; font-weight:700; font-size:1.4rem;
                              color:#F7F5EC; margin:12px 0 2px; }
    .sidebar-logo .tagline{ font-size:.66rem; text-transform:uppercase; letter-spacing:.14em;
                             color:#BFCBA8; }
    .sidebar-rule{ border:none; border-top:1px solid rgba(247,245,236,.25); margin:14px 0 6px; }
    .sidebar-foot{ font-size:.74rem; color:#BFCBA8; line-height:1.5; margin-top:10px; }

    /* ---- card ------------------------------------------------------------ */
    .card{
        background-color: var(--card);
        border: 1px solid var(--card-bd);
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 2px 10px rgba(58,47,37,.06);
        margin-bottom: 12px;
    }

    /* ---- buttons (native = moss primary; secondary = outlined moss) ------- */
    .stButton > button{
        background-color: var(--moss);
        color: #F7F5EC;
        border: none; border-radius: 10px;
        font-family:'Public Sans',sans-serif; font-weight:600;
        padding: 10px 20px;
    }
    .stButton > button:hover{ background-color:#24391F; color:#F7F5EC; }
    .stButton > button[data-testid="stBaseButton-secondary"]{
        background:transparent; color:var(--moss); border:1.5px solid var(--moss);
    }
    .stButton > button[data-testid="stBaseButton-secondary"]:hover{
        background:var(--field); color:var(--moss); border-color:var(--moss);
    }

    /* ---- HTML CTA classes (hero) ----------------------------------------- */
    .btn{ display:inline-block; border-radius:10px; padding:13px 26px;
          font-family:'Public Sans',sans-serif; font-weight:600; font-size:.95rem;
          text-decoration:none; transition: transform .15s ease, box-shadow .15s ease; }
    .btn:hover{ transform: translateY(-2px); }
    .btn-solid{ background:var(--barley); color:#2A2113; box-shadow:0 6px 18px rgba(0,0,0,.25); }
    .btn-ghost{ border:1.5px solid rgba(247,245,236,.7); color:#F7F5EC; }

    /* ---- hero logo badge (Home only) -------------------------------------- */
    /* Small horizontal lockup: the same full-colour medallion as the sidebar,
       sized down, plus the wordmark as real text — sits straight on the hero's
       dark gradient corner, no card around the text. */
    .hero-logo{ position:absolute; top:28px; left:28px; display:flex; align-items:center; gap:14px; }
    .hero-logo .logo-medallion{ width:64px; height:64px; margin:0; }
    .hero-logo .logo-medallion img{ width:50px; }
    .hero-logo .wordmark{ font-family:'Fraunces',serif; font-weight:700; font-size:1.2rem;
                           color:#F7F5EC; text-shadow:0 2px 8px rgba(0,0,0,.35); }

    /* ---- eyebrow pill ---------------------------------------------------- */
    /* margin-top clears the absolutely-positioned .hero-logo badge (top:24px,
       ~86px tall), which otherwise overlaps/clips this pill's left edge. */
    .eyebrow{ display:inline-block; margin-top:56px; font-size:.72rem; letter-spacing:.18em;
              text-transform:uppercase; color:var(--barley);
              border:1px solid rgba(201,162,75,.6); border-radius:999px; padding:5px 14px; }

    /* ---- badge ----------------------------------------------------------- */
    .badge{ display:inline-block; background-color:var(--leaf); color:#F1EFDF;
            padding:4px 12px; border-radius:20px; font-size:12px; font-weight:600;
            margin-right:6px; margin-bottom:6px; }
    .badge.protected{ background-color:var(--barley); color:#2A2113; }

    /* ---- avatar / loop step badge ---------------------------------------- */
    .avatar,.step{ display:inline-flex; align-items:center; justify-content:center;
                   background-color:var(--moss); color:#F7F5EC; border-radius:50%;
                   font-family:'Fraunces',serif; font-weight:600; }
    .avatar{ width:44px; height:44px; font-size:15px; }
    .step{ width:34px; height:34px; font-size:.95rem; }

    /* ---- section heading + dashed rule ----------------------------------- */
    .section-head{ display:flex; align-items:baseline; gap:16px; margin:48px 0 6px; }
    .section-head h2{ font-size:1.9rem; font-weight:600; margin:0; }
    .section-head .tick{ flex:1; border-top:1px dashed #C9C4AC; transform:translateY(-6px); }

    /* ---- field-strip stat band -------------------------------------------- */
    /* single moss tone (was 4 competing shades) so it reads as one band, not a
       stripe, and sits quietly under the dark hero rather than fighting it. */
    .strips{ display:flex; border-radius:14px; overflow:hidden; margin:48px 0 8px;
             box-shadow:0 2px 10px rgba(58,47,37,.08); }
    .strip{ flex:1; padding:26px; background:var(--moss); }
    .strip .num{ font-family:'Fraunces',serif; font-size:2.6rem; font-weight:600;
                 line-height:1; color:var(--barley); }
    .strip .lbl{ font-size:.74rem; text-transform:uppercase; letter-spacing:.13em;
                 margin-top:8px; color:#F1EFDF; opacity:.85; }

    /* ---- loop card ------------------------------------------------------- */
    .loop-card{ background:var(--card); border:1px solid var(--card-bd); border-radius:14px;
                padding:24px 22px 20px; position:relative; height:100%; }
    .loop-card::after{ content:'\\2192'; position:absolute; right:-15px; top:50%;
                       transform:translateY(-50%); color:var(--barley); font-size:1.3rem;
                       font-weight:700; z-index:2; }
    .loop-card.closing::after{ content:'\\21BA'; right:14px; top:14px; transform:none; opacity:.6; }
    .loop-card .step{ margin-bottom:14px; }
    .loop-card h3,.loop-card h4{ font-family:'Fraunces',serif; font-size:1.12rem;
                                 margin:0 0 8px; font-weight:600; }
    .loop-card p{ font-size:.9rem; line-height:1.55; color:#5B5345; margin:0; }

    /* ---- featured seed card ---------------------------------------------- */
    .seed-card{ background:var(--card); border:1px solid var(--card-bd); border-radius:14px;
                overflow:hidden; transition: box-shadow .2s ease, transform .2s ease; height:100%; }
    .seed-card:hover{ box-shadow:0 10px 26px rgba(58,47,37,.12); transform:translateY(-3px); }
    .seed-card .swatch{ height:8px; }
    .seed-card .pad{ padding:18px 20px 20px; }
    .seed-card .county{ font-size:.68rem; letter-spacing:.14em; text-transform:uppercase; color:var(--leaf); }
    .seed-card h4{ font-family:'Fraunces',serif; font-size:1.08rem; margin:6px 0; }
    .seed-card p{ font-size:.86rem; color:#5B5345; line-height:1.5; margin:0 0 12px; }
    .seed-card .meta{ font-size:.78rem; color:#8A8268; }

    /* ---- quote band ------------------------------------------------------ */
    .quote{ background:var(--moss); border-radius:16px; padding:46px 52px;
            margin:48px 0 8px; color:#EFEEDE; }
    .quote blockquote{ font-family:'Fraunces',serif; font-size:1.5rem; line-height:1.45;
                       font-style:italic; font-weight:400; margin:0 0 16px; max-width:32ch; color:#F4F2E4; }
    .quote cite{ font-style:normal; font-size:.85rem; letter-spacing:.1em;
                 text-transform:uppercase; color:var(--barley); }

    /* ---- responsive ------------------------------------------------------ */
    @media (max-width: 880px){
        .strips{ flex-direction:column; }
        .loop-card::after{ display:none; }
    }
    </style>
    """, unsafe_allow_html=True)


def render_sidebar():
    """
    Render the SeedLoop brand block at the top of the sidebar (above the native nav,
    via the flex-order rule in inject_theme). Call this right after inject_theme().
    """
    _logo = _logo_icon_b64()
    if _logo:
        st.sidebar.markdown(
            f'<div class="sidebar-logo">'
            f'<div class="logo-medallion"><img src="data:image/png;base64,{_logo}" alt="" /></div>'
            f'<div class="wordmark">SeedLoop</div>'
            f'<div class="tagline">Midwest Biodistrict Seed Cooperative</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    st.sidebar.markdown(
        '<hr class="sidebar-rule">'
        '<p class="sidebar-foot">Member-governed<br>'
        'Clare · Galway · Limerick · Tipperary</p>',
        unsafe_allow_html=True,
    )


def render_footer():
    """
    Render the footer with the Commons motto and steward credit.
    Call this on every page.
    """
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.caption("🌱 Governed by members, not corporations")
    with col2:
        st.caption(f"Steward: {STEWARD}")
