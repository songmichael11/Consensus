"""
shits broken but im gonna fix it tomorrow morning
"""


import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import requests
import json

SideBarLinks()

# Constants for your API
API_BASE_URL = "http://web-api:4000"  # Your Flask API URL

def update_ngo(ngo_id, update_data):
    """
    Function to update an NGO's information
    """
    try:
        # Make the PUT request to your Flask API
        response = requests.put(
            f"{API_BASE_URL}/ngo/ngos/{ngo_id}",
            json=update_data,  # This automatically sets Content-Type to application/json
            headers={"Content-Type": "application/json"}
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Return the response data
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating NGO: {str(e)}")
        return None

# Example usage in your Streamlit page
def main():
    st.title("Update NGO Information")

    st.button("yo")
    
    # Input for NGO ID
    ngo_id = st.number_input("Enter NGO ID", min_value=1, step=1)
    
    # Input fields for NGO data
    name = st.text_input("NGO Name")
    country = st.text_input("Country")
    website = st.text_input("Website")
    
    if st.button("Update NGO"):
        # Prepare the update data
        update_data = {}
        if name:
            update_data["Name"] = name
        if country:
            update_data["Country"] = country
        if website:
            update_data["Website"] = website
            
        if update_data:  # Only make the request if there's data to update
            result = update_ngo(ngo_id, update_data)
            if result:
                st.success("NGO updated successfully!")
        else:
            st.warning("Please enter at least one field to update")