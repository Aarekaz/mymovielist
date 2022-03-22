import imp
import time

import streamlit as st
from pkg_resources import Distribution
from pyparsing import col

from eda import *
from item_recommender import get_movie_recommendation
from user_recommender import user_recomender


def home():
    st.header("Welcome to My Movie List")
    st.markdown("![](https://media.giphy.com/media/3ohhwDMC187JqL69DG/giphy.gif)")

    selection = st.selectbox(
        "Which type of reccomendation do you want?",
        ["Item Based", "User Based"],
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
            get_movie_recommendation(name, n)

    elif selection == "User Based":
        form = st.form(key="my_form", clear_on_submit=False)

        user = form.number_input("Enter the USER ID you wish to be recommended upon:")

        n = form.slider("How many movies do you want to be recommended?", 0, 50)

        submit_button = form.form_submit_button(label="Give me recommendations!")

        if submit_button:

            with st.spinner("Generating Recommendations..."):
                time.sleep(3)
            st.success("Done!")
            user_recomender(user, n)


def show_viz():
    st.title("Visualizations Based on the Dataset")
    st.subheader(
        "The following visualizations are based on the data in dataset. They have been done based on different scenarios and also on the basis of the value they provide."
    )
    options = st.radio(
        "",
        (
            "Based on Title",
            "Franchise",
            "Language",
            "Release Time",
            "Genre",
            "Earning",
            "Country",
        ),
    )
    if options == "Based on Title":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(" #### Title ")
            st.write(display_title_wordcloud())
        with col2:
            st.markdown(" #### Overview ")
            st.write(display_overview_wordcloud())

    elif options == "Franchise":
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                "The **Harry Potter** Franchise is the most successful movie franchise raking in more than 7.707 billion dollars from 8 movies. The **Star Wars** Movies come in a close second with a 7.403 billion dollars from 8 movies too. **James Bond** is third but the franchise has significantly more movies compared to the others in the list and therefore, a much smaller average gross."
            )
        with col2:
            st.write(display_fanchise())

    elif options == "Language":
        st.write("Distribution of various languages of movie in the dataset")
        st.write(display_language())

    elif options == "Release Time":
        st.write("Distribution of release time of movie in the dataset")
        col1, col2 = st.columns(2)

        with col1:
            st.write(display_release_date())
        with col2:
            st.write(display_release_day())
        col3, col4 = st.columns(2)
        with col3:
            st.write(gross_month())
        with col4:
            st.write(number_by_year())

    elif options == "Genre":
        st.write("Distribution of various genres of movie in the dataset")

        col1, col2 = st.columns(2)

        with col1:
            st.write(display_genre())
        with col2:
            st.write(genre_revenue())
        st.write(genre_roi())

    elif options == "Earning":
        st.write("Visualualization based on Earnings")
        col1, col2 = st.columns(2)

        with col1:
            st.write(movie_roi())

        with col2:
            st.write(earning_graph())
    elif options == "Country":
        st.write("Distribution of various countries of movie in the dataset")
        st.write(map_countries())


def show_data():
    st.title(" A look at the data that we are using for our project")
    st.markdown(
        "The datasets below was obtained through TMDB and IDMB. We also used THe movie lens data into our project. The movies available in this dataset are in correspondence with the movies that are listed in the **MovieLens Latest Full Dataset** comprising of 26 million ratings on 45,000 movies from 27,000 users."
    )
    st.write("The features of the dataset are  ")
    st.markdown(
        """ ### Features

    * **adult:** Indicates if the movie is X-Rated or Adult.
    * **belongs_to_collection:** A stringified dictionary that gives information on the movie series the particular film belongs to.
    * **budget:** The budget of the movie in dollars.
    * **genres:** A stringified list of dictionaries that list out all the genres associated with the movie.
    * **homepage:** The Official Homepage of the move.
    * **id:** The ID of the move.
    * **imdb_id:** The IMDB ID of the movie.
    * **original_language:** The language in which the movie was originally shot in.
    * **original_title:** The original title of the movie.
    * **overview:** A brief blurb of the movie.
    * **popularity:** The Popularity Score assigned by TMDB.
    * **poster_path:** The URL of the poster image.
    * **production_companies:** A stringified list of production companies involved with the making of the movie.
    * **production_countries:** A stringified list of countries where the movie was shot/produced in.
    * **release_date:** Theatrical Release Date of the movie.
    * **revenue:** The total revenue of the movie in dollars.
    * **runtime:** The runtime of the movie in minutes.
    * **spoken_languages:** A stringified list of spoken languages in the film.
    * **status:** The status of the movie (Released, To Be Released, Announced, etc.)
    * **tagline:** The tagline of the movie.
    * **title:** The Official Title of the movie.
    * **video:** Indicates if there is a video present of the movie with TMDB.
    * **vote_average:** The average rating of the movie.
    * **vote_count:** The number of votes by users, as counted by TMDB. """
    )

    # movies = pd.read_csv("EDA_data/movies_metadata.csv", sep=";")
    # st.write(movies.head())

    movies = pd.read_csv("EDA_data/movies_metadata.csv", on_bad_lines="skip")
    st.write(movies.head())

    col1, col2 = st.columns(2)

    rec_movie = pd.read_csv("data/movies.csv", on_bad_lines="skip")
    rec_rating = pd.read_csv("data/ratings.csv", on_bad_lines="skip")

    with col1:
        st.markdown(" #### Movies Dataset ")
        st.write(rec_movie.head())

    with col2:
        st.markdown(" #### Ratings Dataset ")
        st.write(rec_rating.head())
