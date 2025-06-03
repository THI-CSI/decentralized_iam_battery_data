import streamlit as st
import requests
import os

# Dynamic API base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

st.title("BatteryPass Database Viewer")

# Sidebar options to interact with the API
st.sidebar.title("Options")
view_data = st.sidebar.selectbox(
    "What would you like to do?",
    ["View All DIDs", "Retrieve DID Data"]
)

# Function to fetch all DIDs
def list_all_dids():
    url = f"{API_BASE_URL}/batterypass/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code}, {response.text}")
            return []
    except Exception as e:
        st.error(f"Could not connect to the API: {e}")
        return []

# Function to fetch data for a specific DID
def fetch_did_data(did):
    url = f"{API_BASE_URL}/batterypass/{did}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        st.error(f"Could not connect to the API: {e}")
        return None

# View All DIDs
if view_data == "View All DIDs":
    st.header("List of All Available DIDs")
    dids = list_all_dids()
    if dids:
        st.write("Available DIDs in the database:")
        st.write(dids)

# Retrieve and Display Data for a DID
elif view_data == "Retrieve DID Data":
    st.header("Retrieve Data for a Specific DID")
    did_input = st.text_input("Enter a DID to fetch its data:", "")
    if st.button("Fetch Data"):
        if did_input.strip():
            data = fetch_did_data(did_input.strip())
            if data:
                st.json(data)  # Display the data in JSON format
        else:
            st.warning("Please enter a valid DID.")