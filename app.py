import streamlit as st
import pandas as pd
from db import fetch_all, execute_query, fix_sequence
import queries

st.set_page_config(page_title="Food Wastage Management", layout="wide")
st.title("Local Food Wastage Management System")

# Optional: Fix food_id sequence to avoid duplicate key errors
fix_sequence("food_listings", "food_id")

# Sidebar
section = st.sidebar.selectbox("Choose Section", ["Food Listings", "Add Listing", "Insights"])

# View Listings
if section == "Food Listings":
    city_options = fetch_all("SELECT DISTINCT location FROM food_listings")
    if city_options:
        city = st.selectbox("Select City", [r[0] for r in city_options])
        query = """
            SELECT f.food_name, f.quantity, f.expiry_date, p.name AS provider, f.food_type, f.meal_type
            FROM food_listings f
            JOIN providers p ON f.provider_id = p.provider_id
            WHERE f.location = %s
        """
        data = fetch_all(query, (city,))
        df = pd.DataFrame(data, columns=["Food Name", "Quantity", "Expiry", "Provider", "Type", "Meal"])
        st.dataframe(df)
    else:
        st.warning("No food listings available.")

# Add Listing
elif section == "Add Listing":
    with st.form("add_food"):
        name = st.text_input("Food Name")
        qty = st.number_input("Quantity", min_value=1)
        expiry = st.date_input("Expiry Date")

        # Provider dropdown
        providers = fetch_all("SELECT provider_id, name FROM providers")
        provider_options = {f"{name} (ID: {pid})": pid for pid, name in providers}
        provider = st.selectbox("Select Provider", list(provider_options.keys()))
        pid = provider_options[provider]

        # Location dropdown based on provider cities
        cities = fetch_all("SELECT DISTINCT city FROM providers")
        city = st.selectbox("Location", [r[0] for r in cities])

        ptype = st.selectbox("Provider Type", ["Restaurant", "Grocery Store", "Supermarket"])
        ftype = st.selectbox("Food Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        mtype = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snacks"])

        submitted = st.form_submit_button("Add")

        if submitted:
            execute_query("""
                INSERT INTO food_listings 
                (food_name, quantity, expiry_date, provider_id, provider_type, location, food_type, meal_type)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (name, qty, expiry, pid, ptype, city, ftype, mtype))
            st.success("Food listing added successfully!")

# Insights Section
elif section == "Insights":
    st.header("Insights & Analysis")

    with st.expander("Providers & Receivers in Each City"):
        result = queries.providers_and_receivers_by_city()
        st.dataframe(pd.DataFrame(result, columns=["City", "Providers", "Receivers"]))

    with st.expander("Provider Type Contributing the Most Food"):
        result = queries.provider_type_with_most_food()
        st.dataframe(pd.DataFrame(result, columns=["Provider Type", "Total Food Listings"]))

    with st.expander("Contact Info of Providers by City"):
        city = st.text_input("Enter City for Provider Contacts")
        if city:
            result = queries.provider_contacts_by_city(city)
            st.dataframe(pd.DataFrame(result, columns=["Name", "Type", "Contact"]))

    with st.expander("Receivers with Most Food Claims"):
        result = queries.top_receivers_by_claim_count()
        st.dataframe(pd.DataFrame(result, columns=["Receiver Name", "Total Claims"]))

    with st.expander("Total Quantity of Food Available"):
        result = queries.total_food_quantity()
        qty = result[0][0] if result[0][0] is not None else 0
        st.metric(label="Total Food Quantity Available", value=int(qty))

    with st.expander("City with Highest Number of Food Listings"):
        result = queries.city_with_most_food()
        st.dataframe(pd.DataFrame(result, columns=["City", "Listings"]))

    with st.expander("Most Common Food Types Available"):
        result = queries.most_common_food_types()
        st.dataframe(pd.DataFrame(result, columns=["Food Type", "Count"]))

    with st.expander("Food Claims Per Item"):
        result = queries.claims_per_food_item()
        st.dataframe(pd.DataFrame(result, columns=["Food Name", "Claims"]))

    with st.expander("Provider with Highest Completed Claims"):
        result = queries.top_provider_by_completed_claims()
        st.dataframe(pd.DataFrame(result, columns=["Provider Name", "Completed Claims"]))

    with st.expander("Claim Status Breakdown"):
        result = queries.claims_status_breakdown()
        st.dataframe(pd.DataFrame(result, columns=["Status", "Count"]))

    with st.expander("Avg Quantity Claimed Per Receiver"):
        result = queries.avg_quantity_per_receiver()
        avg = result[0][0]
        if avg is not None:
            st.metric("Average Quantity Per Receiver", value=float(round(avg, 2)))
        else:
            st.metric("Average Quantity Per Receiver", value="No data")

    with st.expander("Most Claimed Meal Type"):
        result = queries.most_claimed_meal_type()
        st.dataframe(pd.DataFrame(result, columns=["Meal Type", "Claims"]))

    with st.expander("Total Quantity Donated by Each Provider"):
        result = queries.total_food_by_provider()
        st.dataframe(pd.DataFrame(result, columns=["Provider Name", "Total Donated Quantity"]))
