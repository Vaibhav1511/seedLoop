import html
import streamlit as st
from datetime import datetime, timedelta
from data import list_seeds, STEWARD, get_seed, seed_credits, CURRENT_USER, SEED_CREDITS_INFO
from ui import render_footer, inject_theme

st.set_page_config(page_title="My Exchanges", page_icon=":material/swap_horiz:", layout="wide")

inject_theme()

st.title("My Exchanges")
st.write("Track your seed swaps and exchange requests with other members of the Commons.")

# --- Seed Credits (display-only model) ---
st.subheader("Seed Credits")
_contributed = ["Autumn King Carrot", "Wexford Heritage Oat", "Painted Lady Bean"]
_contributed = [n for n in _contributed if get_seed(n)]
_balance = sum(seed_credits(get_seed(n)) for n in _contributed)
_chips = " ".join(
    f'<span class="badge">{html.escape(n)} · {seed_credits(get_seed(n))}</span>' for n in _contributed
)
st.markdown(
    f'<div class="card">'
    f'<div style="display:flex;align-items:baseline;gap:10px;">'
    f'<span style="font-family:\'Fraunces\',serif;font-size:2.2rem;font-weight:700;color:#2E4A2C;">{_balance}</span>'
    f'<span style="color:#8A8268;text-transform:uppercase;letter-spacing:.1em;font-size:.72rem;">'
    f'credits · {html.escape(CURRENT_USER["name"])}</span></div>'
    f'<div style="margin:10px 0;">{_chips}</div>'
    f'<div style="font-size:0.9rem;color:#5B5345;">Credits are earned by depositing quality seed '
    f'and spent receiving others&rsquo; seed — no cash, no royalties leaving the community.</div>'
    f'</div>',
    unsafe_allow_html=True,
)
with st.expander("How seed credits work"):
    st.caption(SEED_CREDITS_INFO)
st.divider()

# Initialize session state with example exchanges
if "incoming_requests" not in st.session_state:
    st.session_state["incoming_requests"] = [
        {
            "id": 1,
            "requester": "Brigid Ní Fhaoláin",
            "seed_wanted": "Autumn King Carrot",
            "county": "Galway",
            "date": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
            "status": "Pending",
        },
        {
            "id": 2,
            "requester": "Pádraig Flynn",
            "seed_wanted": "Purple Sprouting Broccoli",
            "county": "Tipperary",
            "date": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
            "status": "Pending",
        },
        {
            "id": 3,
            "requester": "Siobhán Murphy",
            "seed_wanted": "Tipperary Gold Tomato",
            "county": "Clare",
            "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
            "status": "Pending",
        },
        {
            "id": 4,
            "requester": "Máire Ó'Brien",
            "seed_wanted": "Irish Lovage",
            "county": "Limerick",
            "date": (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
            "status": "Accepted",
        },
    ]

if "outgoing_requests" not in st.session_state:
    st.session_state["outgoing_requests"] = [
        {
            "id": 101,
            "recipient": "Aoife Kavanagh",
            "seed_requested": "Wexford Heritage Oat",
            "county": "Galway",
            "date": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "status": "Accepted",
        },
        {
            "id": 102,
            "recipient": "Nuala Sullivan",
            "seed_requested": "Painted Lady Bean",
            "county": "Clare",
            "date": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
            "status": "Pending",
        },
    ]

# Status color mapping
status_colors = {
    "Pending": "🟡",
    "Accepted": "🟢",
    "Declined": "🔴",
}

# Helper to update request status
def update_request_status(request_id, new_status, request_type="incoming"):
    if request_type == "incoming":
        for req in st.session_state["incoming_requests"]:
            if req["id"] == request_id:
                req["status"] = new_status
    else:
        for req in st.session_state["outgoing_requests"]:
            if req["id"] == request_id:
                req["status"] = new_status

# Incoming Requests
st.subheader("Incoming Requests")
st.write("Members are asking for seeds from your collection.")

if not st.session_state["incoming_requests"]:
    st.info("No incoming requests yet.")
else:
    for req in st.session_state["incoming_requests"]:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown(
                f"**{req['requester']}** wants **{req['seed_wanted']}**  \n"
                f"From: {req['county']} • Requested: {req['date']}"
            )
        
        with col2:
            st.markdown(f"{status_colors.get(req['status'], '⚪')} **{req['status']}**")
        
        with col3:
            if req["status"] == "Pending":
                if st.button("✓ Accept", key=f"accept_{req['id']}", use_container_width=True):
                    update_request_status(req["id"], "Accepted", "incoming")
                    st.success(f"Accepted {req['requester']}'s request!")
                    st.rerun()
        
        with col4:
            if req["status"] == "Pending":
                if st.button("✗ Decline", key=f"decline_{req['id']}", use_container_width=True):
                    update_request_status(req["id"], "Declined", "incoming")
                    st.warning(f"Declined {req['requester']}'s request.")
                    st.rerun()
        
        st.divider()

# Outgoing Requests
st.subheader("Outgoing Requests")
st.write("Seeds you've asked for from other members.")

if not st.session_state["outgoing_requests"]:
    st.info("You haven't made any outgoing requests yet.")
else:
    for req in st.session_state["outgoing_requests"]:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(
                f"**Requested from {req['recipient']}:** {req['seed_requested']}  \n"
                f"Location: {req['county']} • Requested: {req['date']}"
            )
        
        with col2:
            st.markdown(f"{status_colors.get(req['status'], '⚪')} **{req['status']}**")
        
        st.divider()

# Contact Steward Card
st.divider()
st.subheader("Need Help?")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown(f"""
    ### Contact Your Steward
    
    **{STEWARD}**
    
    Nuala runs the twice-yearly seed swaps and can help coordinate exchanges, resolve questions, and connect you with other growers.
    
    **Seed Swap Locations & Timing:**
    - :primary[:material/agriculture:] **Cloughjordan** (spring swap)
    - :primary[:material/agriculture:] **Limerick** (autumn swap)
    
    These are great opportunities to meet other members, see seeds in person, and build the Commons together.
    """)

with col_right:
    st.markdown("""
    :primary[:material/location_on:] **Cloughjordan**

    Ecovillage community
    
    ---
    
    :primary[:material/location_on:] **Limerick**

    Local venues rotate
    """)

render_footer()
