import streamlit as st
import pandas as pd
from data import SEEDS, list_seeds, STEWARD
from ui import render_footer, inject_theme

st.set_page_config(page_title="List a Seed", page_icon=":material/note_add:", layout="wide")

inject_theme()

st.title("List a Seed")
st.write("Share a locally-saved seed variety with the Commons. Your listing will be reviewed by the Seed Commons Steward before going live.")

st.info(f"**Steward:** {STEWARD} will review all new listings before they appear in the public registry.")

# Initialize session state for listings
if "listings" not in st.session_state:
    st.session_state["listings"] = []

# Prepare options
crop_types = sorted({v.get("crop") for v in SEEDS.values() if v.get("crop")})
counties = ["Clare", "Galway", "Limerick", "Tipperary"]

# Form
st.subheader("Seed Details")

col1, col2 = st.columns(2)
with col1:
    variety_name = st.text_input("Variety name *", placeholder="e.g., Heritage Red Tomato", key="variety_name_input")
with col2:
    latin_name = st.text_input("Latin name", placeholder="e.g., Solanum lycopersicum", key="latin_name_input")

col3, col4 = st.columns(2)
with col3:
    crop_type = st.selectbox("Crop type *", options=crop_types, key="crop_type_select")
with col4:
    selected_counties = st.multiselect("County/ies where grown *", options=counties, key="county_select")

col5, col6 = st.columns(2)
with col5:
    grower_name = st.text_input("Your name (grower) *", placeholder="e.g., Máire Ó'Brien", key="grower_name_input")
with col6:
    quantity = st.text_input("Quantity available (seeds/plants/lbs) *", placeholder="e.g., 50 seeds", key="quantity_input")

st.subheader("Variety Story")
variety_story = st.text_area(
    "Tell us the story of this seed *",
    placeholder="Where did you save it from? Who gave it to you? Why does it matter to the Commons? (2–3 sentences minimum)",
    height=120,
    key="story_textarea"
)

# Submit button
if st.button("Submit listing", type="primary"):
    # Validation
    errors = []
    if not variety_name.strip():
        errors.append("Variety name is required")
    if not crop_type:
        errors.append("Crop type is required")
    if not selected_counties:
        errors.append("At least one county is required")
    if not grower_name.strip():
        errors.append("Grower name is required")
    if not quantity.strip():
        errors.append("Quantity is required")
    if not variety_story.strip() or len(variety_story.strip()) < 10:
        errors.append("Variety story is required (at least 10 characters)")

    if errors:
        st.error("Please fix the following before submitting:\n" + "\n".join([f"• {e}" for e in errors]))
    else:
        # Add to listings
        listing = {
            "Variety Name": variety_name.strip(),
            "Latin Name": latin_name.strip() or "—",
            "Crop Type": crop_type,
            "County/ies": ", ".join(selected_counties),
            "Grower": grower_name.strip(),
            "Quantity": quantity.strip(),
            "Story": variety_story.strip(),
        }
        st.session_state["listings"].append(listing)

        # Confirmation
        st.success("✓ Listing submitted!")
        st.balloons()
        st.markdown(f"Your seed **{variety_name}** has been submitted to {STEWARD} for review. It will appear in the public registry once approved.")

# Display session listings
if st.session_state["listings"]:
    st.divider()
    st.subheader(f"Listings this session ({len(st.session_state['listings'])})")
    
    # Create DataFrame for display
    df = pd.DataFrame(st.session_state["listings"])
    
    # Show table (without the Story column for compact view, but allow expansion)
    st.write("**Submitted listings awaiting review:**")
    display_cols = ["Variety Name", "Latin Name", "Crop Type", "County/ies", "Grower", "Quantity"]
    st.dataframe(df[display_cols], use_container_width=True)
    
    # Show full details in expanders
    st.write("**Full details:**")
    for i, listing in enumerate(st.session_state["listings"], 1):
        with st.expander(f"{i}. {listing['Variety Name']} — {listing['Grower']}"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Variety:** {listing['Variety Name']}")
                st.write(f"**Latin name:** {listing['Latin Name']}")
                st.write(f"**Crop type:** {listing['Crop Type']}")
                st.write(f"**County/ies:** {listing['County/ies']}")
            with col_b:
                st.write(f"**Grower:** {listing['Grower']}")
                st.write(f"**Quantity:** {listing['Quantity']}")
            st.write(f"**Story:** {listing['Story']}")

render_footer()
