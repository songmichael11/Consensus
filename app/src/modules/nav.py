# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


#### ------------------------ General ------------------------
def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


def AboutPageNav():
    st.sidebar.page_link("pages/30_About.py", label="About", icon="🧠")

def FeedNav():
    st.sidebar.page_link("pages/00_Feed.py", label="My Feed")

def PlaygroundNav():
    st.sidebar.page_link("pages/01_Playground.py", label="Data Playground")

# _____ politicians____
def AnalyticsNav():
    st.sidebar.page_link("Home.py", label="Post Analytics")

# change 
def PostGraphsNav():
    if "Politician" in st.session_state['Roles']:
        label = 'Make Post'
    else:
        label = "Saved Graphs"
    st.sidebar.page_link("pages/03_SavedPosts.py", label=label)

def ProfileNav():
    st.sidebar.page_link("Home.py", label="My Profile")

# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=False):
    """
    This function handles adding links to the sidebar of the app based 
    upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=300)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:
        FeedNav()
        PlaygroundNav()
        PostGraphsNav()
        if "Politician" in st.session_state['Roles']:
            AnalyticsNav()
        ProfileNav()

    

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["Roles"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")
