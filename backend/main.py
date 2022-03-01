import streamlit as st

from recommender import get_movie_recommendation

st.set_page_config(
    page_title="My Movie List",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="auto",
)

st.header("Welcome to My Movie List")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

form = st.form(key="my_form", clear_on_submit=True)

name = form.text_input(
    "Enter the name of the movie that you wish to be recommended upon:"
)

n = form.slider("How many movies do you want to be recommended?", 0, 50)

submit_button = form.form_submit_button(label="Give me recommendations!")


if submit_button:
    get_movie_recommendation(name, n)

