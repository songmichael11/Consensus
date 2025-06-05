import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks

# Page setup
st.set_page_config(layout='wide')

# Sidebar
SideBarLinks()

# Load user info from session
user_id = st.session_state.get('UserID', None)
if not user_id:
    st.error("No user logged in. Please return to home page and log in.")
    st.stop()


def getFeed(user_id):
    API_URL = f"http://web-api:4000/feed/posts/{user_id}"
    try:
        response = requests.get(API_URL)
        feed = response.json()
        logger.info(f"Loaded {len(feed)} posts.")
        return feed
    except Exception as e:
        st.error(f"Error loading feed: {e}")
        st.stop()

# Page Title → e.g. "Voter Feed ("Home")"
role = st.session_state["Roles"][0]
st.markdown(f"### {role} Feed")

# Draw posts
feed = getFeed(user_id)


for post in feed:
    # Outer card
    with st.container():
        c1, c2, c3 = st.columns([0.1, 0.7, 0.2])

        with c1:
            # Upvotes, Downvotes, Endorsements
            st.button(f"🟢 {post['NumUpvotes']}", key=f'upvote{post["PostID"]}')
            st.button(f"🔴 {post['NumDownvotes']}", key=f'downvote{post["PostID"]}')
            st.button(f"🔵 {post['NumEndorsements']}", key=f'endorsement{post["PostID"]}')


        with c2:
            # Title, Author, Description
            st.markdown(f"### {post['Title']}")
            st.markdown(f"**{post['author']}**")
            st.markdown(post['Description'])

            # Show more
            st.markdown("**Show more**")

        with c3:
            # Graph (placeholder image — replace with your GraphID renderer)
            st.image("https://via.placeholder.com/300x200?text=Graph")

            # Bookmark button (simple placeholder)
            if post['bookmarked'] == 'Saved':
                bookmark_icon = "🔖"
            else:
                bookmark_icon = "📑"

            st.button(f"{bookmark_icon}", key=f"bookmark_{post['PostID']}")

    # Divider between posts
    st.markdown("---")
