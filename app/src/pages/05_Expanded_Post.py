import logging
logger = logging.getLogger(__name__)

import streamlit as st
import requests
from modules.nav import SideBarLinks
import plotly.graph_objects as go

# page setup
st.set_page_config(layout='wide')

#API requests
def getPostByID(post_id, user_id):
    url = f"http://web-api:4000/expanded_post/post/{post_id}/{user_id}"
    response = requests.get(url)
    return response.json()

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
    API_BASE = "http://web-api:4000/expanded_post/exops"
    url = f"{API_BASE}/{post_id}"
    response = requests.get(url)
    return response.json()

def getQuestions(post_id):
    API_BASE = "http://web-api:4000/expanded_post/questions"
    url = f"{API_BASE}/{post_id}"
    response = requests.get(url)
    return response.json()

def postQuestion(post, body):
    url = f"http://web-api:4000/expanded_post/question/post/{post['PostID']}/user/{st.session_state.get('UserID', None)}"
    return requests.post(url, json=body)

def postAnswer(question, body):
    url = f"http://web-api:4000/expanded_post/answer/question/{question['QuestionID']}/user/{st.session_state.get('UserID', None)}"
    return requests.post(url, json=body)

def postExOp(post, body):
    url = f"http://web-api:4000/expanded_post/exops/post/{post['PostID']}/user/{st.session_state.get('UserID', None)}"
    return requests.post(url, json=body)

# UI rendering
def renderPlotlyGraph(post):
    response = requests.get(f"http://web-api:4000/models/posts/predict/{post['GraphID']}")
    data = response.json()
    fig = go.Figure(go.Scatter(x=data["x_values"], y=data['predictions'], mode="lines+markers"))
    fig.update_layout(title_text=f"{data['x_axis']} vs. GINI", 
                        margin_autoexpand=False,
                        margin=dict(t=75, b=50, l=50, r=10),
                        height=400)
    st.plotly_chart(fig, key=f"plot{post['PostID']}")

# UI components
def renderBookmarkButton(post, mode="default"):
    # Bookmark button (simple placeholder)
    if post['bookmarked'] == 'Saved':
        bookmark_icon = ":material/bookmark_check:"
    else:
        bookmark_icon = ":material/bookmark:"

    if st.button(label=bookmark_icon, type="secondary", key=f"bookmark_{post['PostID']}_{mode}"):
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
        endorsedIcon = ":material/verified:"
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
    with st.container(border=False, height=200):
        for opinion in data:
            with st.container(border=True):
                st.markdown(f"**{opinion['answerAuthor']}**")
                st.write(f"{opinion['BodyText']}")

def renderQuestions(post):
    data = getQuestions(post["PostID"])
    with st.container(border=False, height=200):
        for question in data:
            with st.container(border=True):
                st.markdown(f"**Question:** {question['QuestionText']}")
                if question["AnswerText"] == None:
                    if "Politician" in st.session_state['Roles'] or "Economist" in st.session_state['Roles']:
                        renderAnswerButton(question)
                    else:
                        st.markdown(f"**Unanswered**")
                else:
                    st.markdown(f"**Answer from {question['answerAuthor']}:** " + question["AnswerText"])

def renderQuestionButton(post):
    body = {}
    with st.popover(label="Ask a Question"):
        body["QuestionText"] = st.text_input(label="Question", max_chars=300)
        if st.button("Submit", key="submitQuestion"):
            response = postQuestion(post, body)
            if response.status_code == 200:
                st.badge("Question Submitted!", color="green")
            elif response.status_code == 210:
                st.badge("User has submitted too many questions", color="red")

def renderAnswerButton(question):
    body = {}
    with st.popover(label="Answer a Question"):
        body["AnswerText"] = st.text_input(label="Answer", max_chars=300, key=f"textAnswer{question['QuestionID']}")
        if st.button("Submit", key=f"submitAnswer{question['QuestionID']}"):
            response = postAnswer(question, body)
            if response.status_code == 200:
                st.badge("Answer Submitted!", color="green")
                st.rerun()
            elif response.status_code == 210:
                st.badge("Question has already been answered", color="red")

def renderExpertInputButton(post):
    body = {}
    with st.popover(label="Add Expert Feedback"):
        body["BodyText"] = st.text_input(label="ExpertInput", max_chars=600)
        if st.button("Submit", key="submitFeedback"):
            response = postExOp(post, body)
            if response.status_code == 200:
                st.badge("Feedback Submitted!", color="green")
            elif response.status_code == 210:
                st.badge("User has already submitted feedback", color="orange")


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
        if st.button("Open in Data Playgound"):
            st.session_state['loaded_graph_id'] = post['GraphID']
            st.switch_page("pages/01_Playground.py")

with st.container():
  c3a, c3b = st.columns([0.5, 0.5])
  
  with c3a:
    with st.container(border=True, height=300):
      header_col, button_col = st.columns([0.4, 0.6])
      with header_col:
        st.markdown("###### Expert Opinions")
      with button_col:
        if "Economist" in st.session_state['Roles']:
          renderExpertInputButton(post)
      renderExpertOps(post)

  with c3b:
    with st.container(border=True, height=300):
      header_col, button_col = st.columns([0.5, 0.5])
      with header_col:
        st.markdown("###### Voter Questions")
      with button_col:
        if "Voter" in st.session_state['Roles']:
          renderQuestionButton(post)
      renderQuestions(post)

# button to return to the feed
if st.button("Return to Feed"):
    # Clear the selected post from session state
    if "ExpandedPost" in st.session_state:
        del st.session_state["ExpandedPost"]
    st.switch_page("pages/00_Feed.py")