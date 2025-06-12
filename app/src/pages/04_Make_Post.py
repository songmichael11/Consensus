import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks
import plotly.graph_objects as go
import time

# page setup
st.set_page_config(layout='wide')

def sendPost(body):
    url = f"http://web-api:4000/make_post/post/{st.session_state.get('UserID', None)}"
    return requests.post(url, json=body)

# renders plotly graph from a graphid
def renderPlotlyGraph(graphID):
    response = requests.get(f"http://web-api:4000/models/posts/predict/{graphID}")
    data = response.json()
    fig = go.Figure(go.Scatter(x=data["x_values"], y=data['predictions'], mode="lines+markers"))
    fig.update_layout(title_text=f"{data['x_axis']} vs. GINI", 
                        margin_autoexpand=False,
                        margin=dict(t=75, b=50, l=50, r=10),
                        height=300)
    st.plotly_chart(fig, key=f"plot{graphID}")

# load user info from session
user_id = st.session_state.get('UserID', None)
if not user_id:
    st.error("No user logged in. Please return to home page and log in.")
    if st.button("Return Home"):
        st.switch_page("Home.py")

# load post info from session
graphID = st.session_state.get("PostedGraph", {}).get("graph_id", None)
if not graphID:
    st.error("No graph logged. Please return to the make post page.")
    if st.button("Go back"):
        st.switch_page("pages/03_SavedPosts.py")

# Main rendering here
SideBarLinks()

st.markdown("# Make Post:")

postDraft = {}

with st.container(border=True):
    postDraft["Title"] = st.text_input(label="Title", placeholder="Title Here", label_visibility="hidden", max_chars=255)
    postDraft["Description"] = st.text_area(label="Description", placeholder="Write your Description Here", label_visibility="hidden")
    postDraft["GraphID"] = graphID
    st.write("Your Graph:")
    renderPlotlyGraph(graphID)
    c1, c2 = st.columns([0.87, 0.13])
    with c1:
        if st.button("Return to Saved Posts"):
            if "PostedGraph" in st.session_state:
                del st.session_state["PostedGraph"]
            st.switch_page("pages/03_SavedPosts.py")
    with c2:
        if st.button("Make Post"):
            response = sendPost(postDraft)
            if response.status_code == 200:
                st.badge("Post Created!", color="green")
                with st.spinner(text="Redirecting to feed...", show_time=False):
                    time.sleep(1)
                    if "PostedGraph" in st.session_state:
                        del st.session_state["PostedGraph"]
                    st.switch_page("pages/00_Feed.py")
            else:
                st.badge("Error. Please try again.", color="red")