##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
import streamlit as st
import requests

logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "http://web-api:4000/landing/users/"
def updateSessionState(userID):
    response = requests.get(API_URL + str(userID)).json()
    st.session_state.update(response)
    st.session_state['authenticated'] = True

def getUserNames(role_id):
    response = requests.get(f"{API_URL}/role/{role_id}").json()
    return response

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(page_title="Consensus Login", layout="wide")

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

showSidebarNavigation = False 
# SideBarLinks(show_home=True)
logger.info("Loading the Home page of the app")

a1, a2 = st.columns([0.5, 0.5])
with a1:
    st.image("assets/logo.png", width=800)
with a2: 
    # title
    st.markdown("<h1 style='font-size: 108px; text-align: left'>Consensus</h1>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 40px; color:#aaaaaa; text-align: left; margin-top: -30px; margin-bottom:-40px'>Policy Reimagined.</h1>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Who would you like to log in as?")

    # Login Buttons in three columns
    b1, b2, b3 = st.columns(3)

    with b1:
        voter_names = getUserNames(1)
        voter_name = st.selectbox(label="Voters: ", options=(row["Name"] for row in voter_names))
        if st.button(f"Log in as Voter, {voter_name}", use_container_width=True):
            updateSessionState(1)
            st.success("Logged in as Voter")
            st.switch_page('pages/00_Feed.py')

    with b2:
        politician_names = getUserNames(2)
        politician_name = st.selectbox(label="Politicians: ", options=(row["Name"] for row in politician_names))

        if st.button(f"Log in as Politician, {politician_name}", use_container_width=True):
            updateSessionState(7)
            st.success("Logged in as Politician")
            st.switch_page('pages/00_Feed.py')

    with b3:
        economist_names = getUserNames(3)
        economist_name = st.selectbox(label="Economists: ", options=(row["Name"] for row in economist_names))
        if st.button(f"Log in as Economist, {economist_name}", use_container_width=True):
            updateSessionState(13)
            st.success("Logged in as Economist")
            st.switch_page('pages/00_Feed.py')
