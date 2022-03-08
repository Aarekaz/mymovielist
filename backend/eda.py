import ast
import datetime
import json

import chart_studio
import chart_studio.plotly as py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import seaborn as sns
import streamlit as st
from chart_studio.tools import set_config_file
from IPython.display import HTML, Image
from scipy import stats
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from wordcloud import STOPWORDS, WordCloud
from xgboost import XGBClassifier, XGBRegressor

set_config_file(
    plotly_domain="plotly_domain=https://chart-studio.plotly.com",
    plotly_api_domain="https://api.plotly.com",
)
chart_studio.tools.set_credentials_file(
    username="rounakbanik", api_key="xTLaHBy9MVv5szF4Pwan"
)

sns.set_style("whitegrid")
sns.set(font_scale=1.25)
pd.set_option("display.max_colwidth", 50)

df = pd.read_csv("EDA_data/movies_metadata.csv")


# Data Wrangling

df = df.drop(["imdb_id"], axis=1)
df[df["original_title"] != df["title"]][["title", "original_title"]].head()
df = df.drop("original_title", axis=1)
df[df["revenue"] == 0].shape
df["revenue"] = df["revenue"].replace(0, np.nan)
df["budget"] = pd.to_numeric(df["budget"], errors="coerce")
df["budget"] = df["budget"].replace(0, np.nan)
df[df["budget"].isnull()].shape
df["return"] = df["revenue"] / df["budget"]
df[df["return"].isnull()].shape
df["year"] = pd.to_datetime(df["release_date"], errors="coerce").apply(
    lambda x: str(x).split("-")[0] if x != np.nan else np.nan
)
df["adult"].value_counts()
df = df.drop("adult", axis=1)
base_poster_url = "http://image.tmdb.org/t/p/w185/"
df["poster_path"] = (
    "<img src='" + base_poster_url + df["poster_path"] + "' style='height:100px;'>"
)


# Exploratory Data Analysis

df["title"] = df["title"].astype("str")
df["overview"] = df["overview"].astype("str")

title_corpus = " ".join(df["title"])
overview_corpus = " ".join(df["overview"])


def display_title_wordcloud():
    title_wordcloud = WordCloud(
        stopwords=STOPWORDS, background_color="white", height=2000, width=4000
    ).generate(title_corpus)
    # plt.figure(figsize=(16, 8))
    # plt.imshow(title_wordcloud)
    # plt.axis("off")
    # plt.show()
    st.image(title_wordcloud.to_array())
    st.markdown(
        "The word **Love** is the most commonly used word in movie titles. **Girl**, **Day** and **Man** are also among the most commonly occuring words. This encapsulates the idea of the ubiquitious presence of romance in movies pretty well."
    )


def display_overview_wordcloud():
    overview_wordcloud = WordCloud(
        stopwords=STOPWORDS, background_color="white", height=2000, width=4000
    ).generate(overview_corpus)
    # plt.figure(figsize=(16,8))
    # plt.imshow(overview_wordcloud)
    # plt.axis('off')
    # plt.show()
    st.image(overview_wordcloud.to_array())
    st.markdown(
        "**Life** is the most commonly used word in Movie titles. **One** and **Find** are also popular in Movie Blurbs. Together with **Love**, **Man** and **Girl**, these wordclouds give us a pretty good idea of the most popular themes present in movies. "
    )


# Production Countries

df["production_countries"] = (
    df["production_countries"].fillna("[]").apply(ast.literal_eval)
)
df["production_countries"] = df["production_countries"].apply(
    lambda x: [i["name"] for i in x] if isinstance(x, list) else []
)
s = (
    df.apply(lambda x: pd.Series(x["production_countries"]), axis=1)
    .stack()
    .reset_index(level=1, drop=True)
)
s.name = "countries"
con_df = df.drop("production_countries", axis=1).join(s)
con_df = pd.DataFrame(con_df["countries"].value_counts())
con_df["country"] = con_df.index
con_df.columns = ["num_movies", "country"]
con_df = con_df.reset_index().drop("index", axis=1)
con_df = con_df[con_df["country"] != "United States of America"]

# TODO : Add a bar chart to show the top 10 production countries
# Error in code from the notebook


# Franchise Movies
def display_fanchise():
    df_fran = df[df["belongs_to_collection"].notnull()]
    df_fran["belongs_to_collection"] = (
        df_fran["belongs_to_collection"]
        .apply(ast.literal_eval)
        .apply(lambda x: x["name"] if isinstance(x, dict) else np.nan)
    )
    df_fran = df_fran[df_fran["belongs_to_collection"].notnull()]
    fran_pivot = df_fran.pivot_table(
        index="belongs_to_collection",
        values="revenue",
        aggfunc={"revenue": ["mean", "sum", "count"]},
    ).reset_index()

    st.dataframe(fran_pivot.sort_values("sum", ascending=False).head(10))
    st.markdown(
        "The **Harry Potter** Franchise is the most successful movie franchise raking in more than 7.707 billion dollars from 8 movies. The **Star Wars** Movies come in a close second with a 7.403 billion dollars from 8 movies too. **James Bond** is third but the franchise has significantly more movies compared to the others in the list and therefore, a much smaller average gross."
    )


# language


def display_language():
    df["original_language"].drop_duplicates().shape[0]
    lang_df = pd.DataFrame(df["original_language"].value_counts())
    lang_df["language"] = lang_df.index
    lang_df.columns = ["number", "language"]

    fig = plt.figure(figsize=(12, 5))
    sns.barplot(x="language", y="number", data=lang_df.iloc[1:11])
    st.pyplot(fig)
    st.markdown(
        "Apart from English,**French** and **Italian** are the most commonly occurring languages after English. **Japanese** and **Hindi** form the majority as far as Asian Languages are concerned."
    )


# release Date
month_order = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def get_month(x):
    try:
        return month_order[int(str(x).split("-")[1]) - 1]
    except:
        return np.nan


def get_day(x):
    try:
        year, month, day = (int(i) for i in x.split("-"))
        answer = datetime.date(year, month, day).weekday()
        return day_order[answer]
    except:
        return np.nan


df["day"] = df["release_date"].apply(get_day)
df["month"] = df["release_date"].apply(get_month)


def display_release_date():
    fig = plt.figure(figsize=(12, 6))
    plt.title("Number of Movies released in a particular month.")
    sns.countplot(x="month", data=df, order=month_order)
    st.pyplot(fig)
    st.markdown(
        "It appears that **January** is the most popular month when it comes to movie releases. In Hollywood circles, this is also known as the *the dump month* when sub par movies are released by the dozen. "
    )
    # Average gross for each month.
    month_mean = pd.DataFrame(
        df[df["revenue"] > 1e8].groupby("month")["revenue"].mean()
    )
    month_mean["mon"] = month_mean.index
    fig = plt.figure(figsize=(12, 6))
    plt.title("Average Gross by the Month for Blockbuster Movies")
    sns.barplot(x="mon", y="revenue", data=month_mean, order=month_order)
    st.pyplot(fig)
    st.markdown(
        "We see that the months of **April**, **May** and **June** have the highest average gross among high grossing movies. This can be attributed to the fact that blockbuster movies are usually released in the summer when the kids are out of school and the parents are on vacation and therefore, the audience is more likely to spend their disposable income on entertainment."
    )


def display_release_day():
    fig = plt.figure(figsize=(10, 5))
    plt.title("Number of Movies released on a particular day.")
    sns.countplot(x="day", data=df, order=day_order)
    st.pyplot(fig)
    st.markdown(
        "**Friday** is clearly the most popular day for movie releases. This is understandable considering the fact that it usually denotes the beginning of the weekend. **Sunday** and **Monday** are the least popular days and this can be attributed to the same aforementioned reason."
    )


def number_by_year():
    st.markdown("### No of Movies Prodcyed by year")
    year_count = df.groupby("year")["title"].count()
    fig = plt.figure(figsize=(18, 5))
    year_count.plot()
    st.pyplot(fig)


def display_genre():
    st.markdown("### Categorizarion by Genre")
    df["genres"] = (
        df["genres"]
        .fillna("[]")
        .apply(ast.literal_eval)
        .apply(lambda x: [i["name"] for i in x] if isinstance(x, list) else [])
    )
    s = (
        df.apply(lambda x: pd.Series(x["genres"]), axis=1)
        .stack()
        .reset_index(level=1, drop=True)
    )
    s.name = "genre"
    gen_df = df.drop("genres", axis=1).join(s)
    gen_df["genre"].value_counts().shape[0]
    pop_gen = pd.DataFrame(gen_df["genre"].value_counts()).reset_index()
    pop_gen.columns = ["genre", "movies"]
    fig = plt.figure(figsize=(18, 8))
    sns.barplot(x="genre", y="movies", data=pop_gen.head(15))
    st.pyplot(fig)
    st.markdown(
        "**Drama** is the most commonly occurring genre with almost half the movies identifying itself as a drama film. **Comedy** comes in at a distant second with 25% of the movies having adequate doses of humor. Other major genres represented in the top 10 are Action, Horror, Crime, Mystery, Science Fiction, Animation and Fantasy."
    )
    # genres = ['Drama', 'Comedy', 'Thriller', 'Romance', 'Action', 'Horror', 'Crime', 'Adventure', 'Science Fiction', 'Mystery', 'Fantasy', 'Mystery', 'Animation']
    # pop_gen_movies = gen_df[(gen_df['genre'].isin(genres)) & (gen_df['year'] >= 2000) & (gen_df['year'] <= 2017)]
    # ctab = pd.crosstab([pop_gen_movies['year']], pop_gen_movies['genre']).apply(lambda x: x/x.sum(), axis=1)
    # ctab[genres].plot(kind='line', stacked=False, colormap='jet', figsize=(12,8)).legend(loc='center left', bbox_to_anchor=(1, 0.5))
    # plt.show()
    # st.pyplot()
    violin_genres = [
        "Drama",
        "Comedy",
        "Thriller",
        "Romance",
        "Action",
        "Horror",
        "Crime",
        "Science Fiction",
        "Fantasy",
        "Animation",
    ]
    violin_movies = gen_df[(gen_df["genre"].isin(violin_genres))]
    fig1 = plt.figure(figsize=(18, 8))
    sns.barplot(x="genre", y="revenue", data=violin_movies)
    st.pyplot(fig1)
    st.markdown(
        "**Animation** movies has the largest 25-75 range as well as the median revenue among all the genres plotted. **Fantasy** and **Science Fiction** have the second and third highest median revenue respectively. "
    )

    st.markdown("### Plot by ROI")
    fig2 = plt.figure(figsize=(18, 8))

    fig2, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 8))
    sns.boxplot(x="genre", y="return", data=violin_movies, palette="muted", ax=ax)
    ax.set_ylim([0, 10])
    st.pyplot(fig2)
    st.markdown(
        "From the boxplot, it seems like **Animation** Movies tend to yield the highest returns on average. **Horror** Movies also tend to be a good bet. This is partially due to the nature of Horror movies being low budget compared to Fantasy Movies but being capable of generating very high revenues relative to its budget."
    )


def first_elem_csv(csv):
    if str(csv) == "nan":
        return np.nan
    else:
        return csv.split(",")[0]


def map_countries():
    movies = pd.read_csv("EDA_data/movies.csv", sep=";")
    # Selección del primer país de la lista de países y creación de tabla counts de países
    movies["primaryCountry"] = movies["countries"].apply(first_elem_csv)
    countries_count = movies.groupby("primaryCountry")[["primaryCountry"]].count()
    countries_count.rename(columns={"primaryCountry": "countryCounts"}, inplace=True)
    countries_count.reset_index(inplace=True)

    fig = px.scatter_geo(
        countries_count,
        locations="primaryCountry",
        hover_name="primaryCountry",
        size="countryCounts",
        text="countryCounts",
        projection="equirectangular",
        locationmode="country names",
        template="plotly_dark",  # width=1200, height=600,
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )

    fig.update_traces(
        marker=dict(color="#f5c518", line_width=0, sizeref=0.1, sizemin=5),
        mode="markers+text",
        textfont=dict(size=10),
    )
    return fig
