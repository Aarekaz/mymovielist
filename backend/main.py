import time

import streamlit as st

from eda import *
from item_recommender import get_movie_recommendation

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
st.sidebar.markdown("![](https://media.giphy.com/media/3ohhwDMC187JqL69DG/giphy.gif)")
st.header("Welcome to My Movie List")


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

form = st.form(key="my_form", clear_on_submit=False)

name = form.text_input(
    "Enter the name of the movie that you wish to be recommended upon:"
)

n = form.slider("How many movies do you want to be recommended?", 0, 50)

submit_button = form.form_submit_button(label="Give me recommendations!")


if submit_button:

    with st.spinner("Calculating Recommendations..."):
        time.sleep(3)
    st.success("Done!")
    new_n = n
    get_movie_recommendation(name, n)

# display_title_wordcloud()
# display_overview_wordcloud()
# display_fanchise()
display_language()
display_release_date()
display_release_day()
number_by_year()

display_genre()

st.write(map_countries())
