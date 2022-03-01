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


get_movie_recommendation(
    st.text_input(
        "Enter the name of the movie that you wish to be recommended upon:",
        key="movie_name",
    )
)


