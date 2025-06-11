import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks
import plotly.graph_objects as go

# page setup
st.set_page_config(layout='wide')

#API requests
# update a post's upvotes, downvotes, or endorsements
# type can be either a put or delete, and metric can be either upvote, downvote, or endorsement
def updatePostUtils(type, metric, post_id, user_id):
    API_BASE = "http://web-api:4000/post_utils"
    url = f"{API_BASE}/post/{post_id}/{metric}/{user_id}"
    if type == "put":
        return requests.put(url)
    else:
        return requests.delete(url)

def getExpertOpinions(post_id):
    API_BASE = "http://web-api:4000/feed/exops"
    url = f"{API_BASE}/{post_id}"
    response = requests.get(url)
    return response.json()

def getQuestions(post_id):
    API_BASE = "http://web-api:4000/feed/questions"
    url = f"{API_BASE}/{post_id}"
    response = requests.get(url)
    return response.json()

def renderPlotlyGraph(post):
    response = requests.get(f"http://web-api:4000/models/posts/predict/{post['GraphID']}")
    data = response.json()
    fig = go.Figure(go.Scatter(x=data["x_values"], y=data['predictions'], mode="lines+markers"))
    fig.update_layout(title_text=f"{data['x_axis']} vs. GINI", 
                        margin_autoexpand=False,
                        margin=dict(t=75, b=50, l=10, r=10),
                        height=400)
    st.plotly_chart(fig, key=f"plot{post['PostID']}")

# UI components
def renderBookmarkButton(post, mode="default"):
    # Bookmark button (simple placeholder)
    if post['bookmarked'] == 'Saved':
        bookmark_icon = "💾"
    else:
        bookmark_icon = ":("

    if st.button(f"{bookmark_icon}", key=f"bookmark_{post['PostID']}_{mode}"):
        if post['bookmarked'] == "Saved":
            response = updatePostUtils("delete", "bookmark", post["PostID"], user_id)
        else:
            response = updatePostUtils("put", "bookmark", post["PostID"], user_id)

        if response.status_code == 200:
            st.rerun()

def renderUpvotesDownvotes(post, mode="default"):
    # Upvotes, Downvotes, Endorsements
    with st.container():
        if (post["upvoted"]) == "Upvoted":
            upvoteIcon = "⬆"
        else:
            upvoteIcon = "⇧"
        if (post["downvoted"]) == "Downvoted":
            downvoteIcon = "⬇"
        else:
            downvoteIcon = "⇩"
        if (post["endorsed"]) == "Endorsed":
            endorsedIcon = "✅"
        else:
            endorsedIcon = "✔️"
        
        if st.button(label=upvoteIcon, key=f'upvote{post["PostID"]}_{mode}'):
            if post['upvoted'] == "Upvoted":
                response = updatePostUtils("delete", "upvote", post["PostID"], user_id)
            else:
                response = updatePostUtils("put", "upvote", post["PostID"], user_id)

            if response.status_code == 200:
                st.rerun()

        st.html(f"<p style='font-size: 30px; text-align: left'>{str(post['karma'])}</p>")
        if st.button(label=downvoteIcon, key=f'downvote{post["PostID"]}_{mode}'):
            if post['downvoted'] == "Downvoted":
                response = updatePostUtils("delete", "downvote", post["PostID"], user_id)
            else:
                response = updatePostUtils("put", "downvote", post["PostID"], user_id)

            if response.status_code == 200:
                st.rerun()

def renderEndorsement(post):
    if (post["endorsed"]) == "Endorsed":
        endorsedIcon = "✅"
    else:
        endorsedIcon = "✔️"

    if "Politician" in st.session_state['Roles']:
        if st.button(label=endorsedIcon, key=f'endorsement{post["PostID"]}', type='secondary'):
            if post['endorsed'] == "Endorsed":
                response = updatePostUtils("delete", "endorsement", post["PostID"], user_id)
            else:
                response = updatePostUtils("put", "endorsement", post["PostID"], user_id)

            if response.status_code == 200:
                st.rerun()
    else:
        st.html(f"<p style='font-size: 20px; margin-left: 10px; margin-bottom: -5px; margin-right:-5px'>✅</p>")

def renderExpertOps(post):
    data = getExpertOpinions(post["PostID"])
    with st.container(border=True, height=200):
        for opinion in data:
            st.markdown(f"**{opinion['answerAuthor']}**")
            st.write(f"{opinion['BodyText']}")

def renderQuestions(post):
    data = getQuestions(post["PostID"])
    with st.container(border=True, height=200):
        for question in data:
            st.write(f"{question['QuestionText']}")

def getPostByID(post_id, user_id):
    url = f"http://web-api:4000/feed/post/{post_id}/{user_id}"
    response = requests.get(url)
    return response.json()

# load user info from session
user_id = st.session_state.get('UserID', None)
if not user_id:
    st.error("No user logged in. Please return to home page and log in.")
    if st.button("Return Home"):
        st.switch_page("Home.py")
# load post info from session
post_id = st.session_state.get("ExpandedPost", {}).get("PostID", None)
if not post_id:
    st.error("No post logged. Please return to the feed.")
    st.stop()

post = getPostByID(post_id, user_id)


# Main rendering here
SideBarLinks()

with st.container():
    c1a, c1b = st.columns([0.1, 0.9], vertical_alignment="bottom")
    with c1a:
        renderUpvotesDownvotes(post)
    with c1b:
        c1ba, c1bb = st.columns([0.9, 0.1])
        with c1ba:
            st.markdown(f"# {post['Title']}")
            st.markdown(f"by **{post['author']}**")
        with c1bb:
            renderBookmarkButton(post)

        with st.container():
            c1a, c1b = st.columns([0.1, 0.9], vertical_alignment="bottom")

            with c1a:
                renderEndorsement(post)
            with c1b:
                st.html(f"<p style='font-size: 15px; text-align: left; margin-left: -60px; margin-bottom: -10px'>{str(post['NumEndorsements'])} Endorsements</p>")

with st.container():
    c2a, c2b = st.columns([0.5, 0.5])
    with c2a:
        with st.container(border=True, height=400):
            st.write(post["Description"])
    with c2b:
        renderPlotlyGraph(post)

with st.container():
    c3a, c3b = st.columns([0.5, 0.5])
    with c3a:
        with st.container(border=True, height=300):
            st.markdown("#### Expert Opinions")
            renderExpertOps(post)
    with c3b:
        with st.container(border=True, height=300):
            st.markdown('### Q&A')
            renderQuestions(post)

# button to return to the feed
if st.button("Return to Feed"):
    # Clear the selected post from session state
    if "ExpandedPost" in st.session_state:
        del st.session_state["ExpandedPost"]
    st.switch_page("pages/00_Feed.py")