import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks
import plotly.graph_objects as go

# page setup
st.set_page_config(layout='wide')

# load user info from session
user_id = st.session_state.get('UserID', None)
if not user_id:
    st.error("No user logged in. Please return to home page and log in.")
    if st.button("Return Home"):
        st.switch_page("Home.py")


# requests
# gets the saved graphs by calling the saved graphs route
def getSavedGraphs(user_id):
    API_URL = f"http://web-api:4000/playground/saved/{user_id}"
    try:
        response = requests.get(API_URL)
        graphs = response.json()
        logger.info(f"Loaded {len(graphs)} posts.")
        return graphs['saved_graphs']
    except Exception as e:
        st.error(f"Error loading feed: {e}")
        st.stop()

# sidebar
SideBarLinks()

#page title
st.markdown(f"### Make a Post")

graphs = getSavedGraphs(user_id)

for graph in graphs:
    with st.container(border=True):
        st.write(graph['name'])