import streamlit as st
from store import Store

st.set_page_config(page_title="Shoptimal", layout="centered")
st.title("🛒 Shoptimal Grocery Sorter")

store_names = ["Tesco", "Sainsbury's"]

# Initialize stores in session state
if "stores" not in st.session_state:
    st.session_state.stores = {name: Store(name) for name in store_names}

items_input = st.text_area("Enter items (comma-separated)")
store_name = st.selectbox("Select store", store_names)
store = st.session_state.stores[store_name]

# Parse items
items = [i.strip() for i in items_input.split(",") if i.strip()]

# Track unknown items and their inputs
if "unknown_aisles" not in st.session_state:
    st.session_state.unknown_aisles = {}

# Step 1: Detect unknown items
unknown_items = [i for i in items if store.get_aisle(i) is None]

# Step 2: Ask user for aisles for unknown items
for item in unknown_items:
    if item not in st.session_state.unknown_aisles:
        st.session_state.unknown_aisles[item] = 1  # default value
    st.session_state.unknown_aisles[item] = st.number_input(
        f"Enter aisle for '{item}'", min_value=1, step=1, key=f"{store_name}_{item}"
    )

# Step 3: Only sort once all unknown aisles have inputs
if st.button("Sort"):
    # Update SQLite with unknown items
    for item, aisle in st.session_state.unknown_aisles.items():
        store.add_item(item, aisle)

    # Clear the session state for next input
    st.session_state.unknown_aisles = {}

    # Sort items
    sorted_items = store.sort_items(items)
    st.subheader("Sorted Grocery List")
    for item, aisle in sorted_items:
        st.write(f"{item} (Aisle {aisle})")
