import streamlit as st
from store import Store

st.set_page_config(page_title="Shoptimal", layout="centered")
st.title("🛒 Shoptimal Grocery Sorter")

store_names = ["Tesco", "Sainsbury's"]

# Session state to keep Store objects alive
if "stores" not in st.session_state:
    st.session_state.stores = {name: Store(name) for name in store_names}

items_input = st.text_area("Enter items (comma-separated)")
store_name = st.selectbox("Select store", store_names)

if st.button("Sort"):
    if not items_input.strip():
        st.warning("Please enter at least one item.")
    else:
        items = [i.strip() for i in items_input.split(",")]
        store = st.session_state.stores[store_name]

        # Define how to get aisle input from Streamlit UI
        def aisle_input_func(item):
            return st.number_input(f"Enter aisle for '{item}'", min_value=1, step=1, key=f"{store_name}_{item}")

        sorted_items = store.sort_items(items, aisle_input_func)

        st.subheader("Sorted Grocery List")
        for item, aisle in sorted_items:
            st.write(f"{item} (Aisle {aisle})")
