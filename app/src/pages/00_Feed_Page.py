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

def getFeed(user_id, params):
    API_URL = f"http://web-api:4000/feed/posts/{user_id}"

    try:
        response = requests.get(API_URL, params=params)
        feed = response.json()
        logger.info(f"Loaded {len(feed)} posts.")
        return feed
    except Exception as e:
        st.error(f"Error loading feed: {e}")
        st.stop()

def getParams(sort, filter, search):
    params = {}
    if sort != "Newest":
        params["sort_by"] = sort.lower()
    if filter != "All":
        params["filter_by"] = filter.lower()
    if search:
        params["search"] = search
    
    return params

# Page Title → e.g. "Voter Feed ("Home")"
st.markdown(f"### {st.session_state['Roles'][0]} Feed")

header_col1, header_col2, header_col3 = st.columns([1, 1, 2])

with header_col1:
    sort = st.selectbox("Sort by…", ["Newest", "Oldest", "Top", "Bottom"])

with header_col2:
    filter = st.selectbox("Filter by…", ["All", "Following", "Saved"])

with header_col3:
    search = st.text_input("Search")

#get parameters
params = getParams(sort, filter, search)
# Draw posts
feed = getFeed(user_id, params)

for post in feed:
    # Outer card
    with st.container():
        c1, c2, c3 = st.columns([0.1, 0.6, 0.3], vertical_alignment="center")

        with c1:
                # Upvotes, Downvotes, Endorsements
                with st.container():
                    if (post["upvoted"]) == "Upvoted":
                        upvoteIcon = "🔼"
                    else:
                        upvoteIcon = "🔺"
                    if (post["downvoted"]) == "Downvoted":
                        downvoteIcon = "🔽"
                    else:
                        downvoteIcon = "🔻"
                    if (post["endorsed"]) == "Endorsed":
                        endorsedIcon = "✅"
                    else:
                        endorsedIcon = "✔️"
                    
                    st.button(label=upvoteIcon, key=f'upvote{post["PostID"]}')  
                    st.html(f"<p style='font-size: 30px; text-align: right; margin-right: 60px'>{str(post['karma']).strip()}</p>")
                    st.button(label=downvoteIcon, key=f'downvote{post["PostID"]}')
                with st.container():
                    st.button(label=endorsedIcon, key=f'endorsement{post["PostID"]}')

        with c2:
            # Title, Author, Description
            st.markdown(f"### {post['Title']}")
            st.markdown(f"**{post['author']}**")
            st.markdown(post['Description'])

            # Show more
            st.markdown("**Show more**")

        with c3:
            # Bookmark button (simple placeholder)
            if post['bookmarked'] == 'Saved':
                bookmark_icon = "Bookmarked"
            else:
                bookmark_icon = "Not Bookmarked"

            st.button(f"{bookmark_icon}", key=f"bookmark_{post['PostID']}")

            # Graph (placeholder image — replace with your GraphID renderer)
            st.image("assets/posts/placeholderGraph.gif")

    # Divider between posts
    st.markdown("---")
