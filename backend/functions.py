import imp
import time

import streamlit as st

from eda import *
from item_recommender import get_movie_recommendation
from user_recommender import get_user_recommendation


def home():
    st.header("Welcome to My Movie List")
    st.markdown("![](https://media.giphy.com/media/3ohhwDMC187JqL69DG/giphy.gif)")

    selection = st.selectbox(
        "Which type of reccomendation do you want?",
        ["Item Based", "User Based", "Hybrid"],
    )
    if selection == "Item Based":
        form = st.form(key="my_form", clear_on_submit=False)

        name = form.text_input(
            "Enter the name of the movie that you wish to be recommended upon:"
        )

        n = form.slider("How many movies do you want to be recommended?", 0, 50)

        submit_button = form.form_submit_button(label="Give me recommendations!")

        if submit_button:

            with st.spinner("Generating Recommendations..."):
                time.sleep(3)
            st.success("Done!")
            new_n = n
            get_movie_recommendation(name, n)

    elif selection == "User Based":
        form = st.form(key="my_form", clear_on_submit=False)

        user = form.text_input("Enter the USER ID you wish to be recommended upon:")

        n = form.slider("How many movies do you want to be recommended?", 0, 50)

        submit_button = form.form_submit_button(label="Give me recommendations!")

        if submit_button:

            with st.spinner("Generating Recommendations..."):
                time.sleep(3)
            st.success("Done!")
            get_user_recommendation(user, n)

    elif selection == "Hybrid":
        st.write("Hybrid")


def show_data():
    st.markdown(
        "The dataset below was obtained through the TMDB API. The movies available in this dataset are in correspondence with the movies that are listed in the **MovieLens Latest Full Dataset** comprising of 26 million ratings on 45,000 movies from 27,000 users."
    )
    #     st.write("The features of the dataset are  ")
    #     st.markdown(
    #         """ ### Features

    # * **adult:** Indicates if the movie is X-Rated or Adult.
    # * **belongs_to_collection:** A stringified dictionary that gives information on the movie series the particular film belongs to.
    # * **budget:** The budget of the movie in dollars.
    # * **genres:** A stringified list of dictionaries that list out all the genres associated with the movie.
    # * **homepage:** The Official Homepage of the move.
    # * **id:** The ID of the move.
    # * **imdb_id:** The IMDB ID of the movie.
    # * **original_language:** The language in which the movie was originally shot in.
    # * **original_title:** The original title of the movie.
    # * **overview:** A brief blurb of the movie.
    # * **popularity:** The Popularity Score assigned by TMDB.
    # * **poster_path:** The URL of the poster image.
    # * **production_companies:** A stringified list of production companies involved with the making of the movie.
    # * **production_countries:** A stringified list of countries where the movie was shot/produced in.
    # * **release_date:** Theatrical Release Date of the movie.
    # * **revenue:** The total revenue of the movie in dollars.
    # * **runtime:** The runtime of the movie in minutes.
    # * **spoken_languages:** A stringified list of spoken languages in the film.
    # * **status:** The status of the movie (Released, To Be Released, Announced, etc.)
    # * **tagline:** The tagline of the movie.
    # * **title:** The Official Title of the movie.
    # * **video:** Indicates if there is a video present of the movie with TMDB.
    # * **vote_average:** The average rating of the movie.
    # * **vote_count:** The number of votes by users, as counted by TMDB. """
    # )

    # movies = pd.read_csv("EDA_data/movies_metadata.csv", sep=";")
    # st.write(movies.head())

    ratings = pd.read_csv("EDA_data/movies_metadata.csv", sep=";")
    st.write(ratings.head())
