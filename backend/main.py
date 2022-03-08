import time

import streamlit as st

from functions import *

st.set_page_config(
    page_title="My Movie List",
    page_icon="🖖",
    layout="wide",
    initial_sidebar_state="auto",
)

st.sidebar.title("My Movie List")
st.sidebar.write(
    "My Movie List is a movie recommendation system based on item based collaborative filtering algorithm"
)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

menu = st.sidebar.radio(
    "",
    ("Intro", "Visuwalizations", "View DataSets"),
)

st.sidebar.markdown("---")
st.sidebar.write(
    "Anurag Dhungana | Apurba Shrestha | Prakriti Bista | Siddhartha Shrestha | 2022"
)

if menu == "Intro":
    home()

elif menu == "Visuwalizations":
    st.write("Show Visulaizations")

elif menu == "View DataSets":
    st.write("In progress")

# display_title_wordcloud()
# display_overview_wordcloud()
# display_fanchise()
# display_language()
# display_release_date()
# display_release_day()
# number_by_year()

# display_genre()

# st.write(map_countries())
