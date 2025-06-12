import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About this App")

st.markdown(
    """
    Policy is often black box and inaccesible, frequently missing data-backed evidence or voter feedback.
    Our app, **Consesus**, fixes that. 
    As the "Stack Overflow of Policy," our app centers around a feed of proposed policies, which all users can interact with.
    - Politicians can make policy posts which always come with machine-learning driven graphs showing how their policies will affect 
    the GINI Index, a measure of wealth inequality. 
    - Voters can ask questions, save, and upvote or downvote posts, allowing them to give feedback and be more in tune with new policy proposals. 
    - Economists can fact-check posts and have access to more advanced machine learning models, allowing them to see how policy proposals will 
    affect communities more in-depth. \n
    Finally, all users also have access to the data playground, where they can play around with how changing economic metrics, such as inflation or 
    government spending on health, can affect the GINI index of a country.
    """
)

# Add a button to return to home page
if st.button("Return Home and Explore our App!", type="primary"):
    st.switch_page("Home.py")