##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://web-api:4000/landing/users/"
def updateSessionState(userID):
    response = requests.get(API_URL + str(userID)).json()
    st.session_state.update(response)
    st.session_state['authenticated'] = True

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(page_title="Consensus Login", layout="wide")

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False
# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)
logger.info("Loading the Home page of the app")

# title
st.markdown("<h1 style='font-size: 72px; text-align: center;'>Consensus</h1>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### Who would you like to log in as?")

# Login Buttons in three columns
b1, b2, b3 = st.columns(3)

with b1:
    if st.button("Log in as Voter,\nPrince Maximilian", use_container_width=True):
        updateSessionState(1)
        st.success("Logged in as Voter")
        st.switch_page('pages/00_Feed.py')

with b2:
    if st.button("Log in as Politician,\nJT Nance", use_container_width=True):
        updateSessionState(7)
        st.success("Logged in as Politician")
        st.switch_page('pages/00_Feed.py')

with b3:
    if st.button("Log in as Economist,\nEmeka Okonkwo", use_container_width=True):
        updateSessionState(13)
        st.success("Logged in as Economist")
        st.switch_page('pages/00_Feed.py')
