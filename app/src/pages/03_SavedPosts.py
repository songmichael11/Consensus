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

# UI ----------------------
def renderPlotlyGraph(graphID):
    response = requests.get(f"http://web-api:4000/models/posts/predict/{graphID}")
    data = response.json()
    fig = go.Figure(go.Scatter(x=data["x_values"], y=data['predictions'], mode="lines+markers"))
    fig.update_layout(title_text=f"{data['x_axis']} vs. GINI", 
                        margin_autoexpand=False,
                        margin=dict(t=75, b=50, l=10, r=10),
                        height=300)
    st.plotly_chart(fig, key=f"plot{graphID}")

# sidebar
SideBarLinks()

#page title
st.markdown(f"### Make a Post")

graphs = getSavedGraphs(user_id)

for graph in graphs:
    with st.container(border=True):
        c0, c1, c2 = st.columns([0.1, 0.4, 0.5])
        with c1:
            st.markdown(f"## {graph['name']}")
            st.markdown(f"#### {graph['date_saved'][:-9]}")
            if st.button("Open in Data Playground", key=f"dataPlaygroundButton{graph['graph_id']}"):
                st.session_state['loaded_graph_id'] = graph['graph_id']
                st.switch_page("pages/01_Playground.py")

            if st.button("Make Post", key=f"makePost{graph['graph_id']}"):
                st.session_state["PostedGraph"] = graph
                st.switch_page("pages/04_Make_Post.py")
            
        with c2:
            renderPlotlyGraph(graph['graph_id'])
