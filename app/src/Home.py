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

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title('CS 4973 Sample DoC Project App')
st.write('\n\n')
st.write('### 2025 Summer 1 Dialogue of Civilizations')
st.write('\n')
st.write('#### HI! As which user would you like to log in?')

st.markdown("---")
st.markdown("### Who would you like to log in as?")

if st.button('Act as Mohammad, an USAID worker', 
            type = 'primary', 
            use_container_width=True):
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'usaid_worker'
    st.session_state['first_name'] = 'Mohammad'
    st.switch_page('pages/10_USAID_Worker_Home.py')

with b1:
    if st.button("Log in as Voter,\nPrince Maximilian", use_container_width=True):
        updateSessionState(1)
        st.success("Logged in as Voter")
        st.switch_page('pages/00_Feed_Page.py')

with b2:
    if st.button("Log in as Politician,\nJT Nance", use_container_width=True):
        updateSessionState(2)
        st.success("Logged in as Politician")
        st.switch_page('pages/00_Feed_Page.py')

with b3:
    if st.button("Log in as Economist,\nEmeka Okonkwo", use_container_width=True):
        updateSessionState(3)
        st.success("Logged in as Economist")
        st.switch_page('pages/00_Feed_Page.py')