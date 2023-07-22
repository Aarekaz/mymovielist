import ast
import datetime
import json
from tarfile import DEFAULT_FORMAT

import chart_studio
import chart_studio.plotly as py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objs as go
import seaborn as sns
import streamlit as st
from chart_studio.tools import set_config_file
from IPython.display import HTML, Image
from scipy import stats
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import (GradientBoostingClassifier,
                              GradientBoostingRegressor)
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


# Data Wrangling
df = pd.read_csv("EDA_data/movies_metadata.csv")
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
    @st.cache
    def load_title():
        title_wordcloud = WordCloud(
            stopwords=STOPWORDS, background_color="black", height=2000, width=4000
        ).generate(title_corpus)
        title_array = title_wordcloud.to_array()
        return title_array

    title_array = load_title()
    # plt.figure(figsize=(16, 8))
    # plt.imshow(title_wordcloud)
    # plt.axis("off")
    # plt.show()
    st.image(title_array)
    st.markdown(
        "The word **Love** is the most commonly used word in movie titles. **Girl**, **Day** and **Man** are also among the most commonly occuring words. This encapsulates the idea of the ubiquitious presence of romance in movies pretty well."
    )


def display_overview_wordcloud():
    @st.cache
    def load_overview():
        overview_wordcloud = WordCloud(
            stopwords=STOPWORDS, background_color="black", height=2000, width=4000
        ).generate(overview_corpus)
        overview_array = overview_wordcloud.to_array()
        return overview_array

    overview_array = load_overview()
    # plt.figure(figsize=(16,8))
    # plt.imshow(overview_wordcloud
    # plt.axis('off')
    # plt.show()
    st.image(overview_array)
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
    @st.cache
    def disp_dffran():
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
        frant_sort = fran_pivot.sort_values("sum", ascending=False).head(10)
        return frant_sort

    fran_sort = disp_dffran()

    st.dataframe(fran_sort)


# language


def display_language():

    df["original_language"].drop_duplicates().shape[0]
    lang_df = pd.DataFrame(df["original_language"].value_counts())
    lang_df["language"] = lang_df.index
    lang_df.columns = ["number", "language"]

    fig = plt.figure(figsize=(12, 5))
    bar = sns.barplot(x="language", y="number", data=lang_df.iloc[1:11])
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
    st.title("Number of Movies released in a particular month.")
    sns.countplot(x="month", data=df, order=month_order)
    st.pyplot(fig)
    st.markdown(
        "It appears that **January** is the most popular month when it comes to movie releases. In Hollywood circles, this is also known as the *the dump month* when sub par movies are released by the dozen. "
    )


def gross_month():
    # Average gross for each month.
    month_mean = pd.DataFrame(
        df[df["revenue"] > 1e8].groupby("month")["revenue"].mean()
    )
    month_mean["mon"] = month_mean.index
    fig = plt.figure(figsize=(12, 6))
    str.title("Average Gross by the Month for Blockbuster Movies")
    sns.barplot(x="mon", y="revenue", data=month_mean, order=month_order)
    st.pyplot(fig)
    st.markdown(
        "We see that the months of **April**, **May** and **June** have the highest average gross among high grossing movies. This can be attributed to the fact that blockbuster movies are usually released in the summer when the kids are out of school and the parents are on vacation and therefore, the audience is more likely to spend their disposable income on entertainment."
    )


def display_release_day():
    fig = plt.figure(figsize=(10, 5))
    st.title("Number of Movies released on a particular day.")
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


# Genre


# def grouppingGenres(genre):
#     if (genre == "Biography") | (genre == "Documentary"):
#         return "Bio-Documentary"
#     elif genre == "Crime":
#         return "Thriller"
#     elif genre == "Fantasy":
#         return "Adventure"
#     elif genre == "Family":
#         return "Adventure"
#     else:
#         return


# def primaryGenre(movies):

#     movies["primaryGenre"] = movies["genres"].apply(first_elem_csv)
#     movies["primaryGenre"] = movies["primaryGenre"].apply(grouppingGenres)

#     return


# def display_genre():
#     movies = pd.read_csv("EDA_data/movies.csv", sep=";")
#     # Preparar el dataset
#     movies = primaryGenre(movies)

#     # Crear la tabla adecuada para el bar stick de plotly
#     genres_by_year = (
#         movies.groupby(["year", "primaryGenre"])[["primaryGenre"]].count().unstack().T
#     )
#     genres_by_year.index = genres_by_year.index.droplevel()
#     genres_by_year.columns = genres_by_year.columns.astype(int)

#     # Ordenar el df por la nueva columna total
#     genres_by_year["TOTAL"] = genres_by_year.sum(axis=1)
#     genres_by_year.sort_values(by=["TOTAL"], inplace=True, ascending=False)
#     genres_by_year = genres_by_year[genres_by_year["TOTAL"] > 1]

#     x = genres_by_year.index

#     trace1 = {
#         "x": x,
#         "y": genres_by_year[2014],
#         "name": "2014",
#         "type": "bar",
#         "marker": {"color": "#F52E18"},
#     }

#     trace2 = {
#         "x": x,
#         "y": genres_by_year[2015],
#         "name": "2015",
#         "type": "bar",
#         "marker": {"color": "#F52E18"},
#     }

#     trace3 = {
#         "x": x,
#         "y": genres_by_year[2016],
#         "name": "2016",
#         "type": "bar",
#         "marker": {"color": "#F55418"},
#     }

#     trace4 = {
#         "x": x,
#         "y": genres_by_year[2017],
#         "name": "2017",
#         "type": "bar",
#         "marker": {"color": "#F57A18"},
#     }

#     trace5 = {
#         "x": x,
#         "y": genres_by_year[2018],
#         "name": "2018",
#         "type": "bar",
#         "marker": {"color": "#F59F18"},
#     }

#     trace6 = {
#         "x": x,
#         "y": genres_by_year[2019],
#         "name": "2019",
#         "type": "bar",
#         "marker": {
#             "color": "#F5C518"
#         },  ## Colores 2019-2014: '#F5184F', '#F52E18', '#F55418', '#F57A18', '#F59F18', '#F5C518'
#     }

#     data = [trace6, trace5, trace4, trace3, trace2, trace1]

#     layout = {
#         "xaxis": {"title": ""},
#         "font": {"family": "Roboto", "size": 16},
#         "barmode": "stack",
#         "template": "plotly_dark",
#         "plot_bgcolor": "rgba(50,50,50,1)",
#     }

#     fig = go.Figure(data=data, layout=layout)
#     return fig


# Countries


def first_elem_csv(csv):
    if str(csv) == "nan":
        return np.nan
    else:
        return csv.split(",")[0]


def map_countries():
    movies = pd.read_csv("EDA_data/movies.csv", sep=";")

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


def movie_roi():
    movies = pd.read_csv("EDA_data/movies.csv", sep=";")
    plt.style.use("dark_background")

    # Preparing data
    n_mvps = 10
    mvps_roi = movies[(movies.roi < 30)][["englishTitle", "roi"]].sort_values(
        by="roi", ascending=False
    )[:n_mvps]
    mvps_roi

    fig, ax = plt.subplots(figsize=(9, 5.5))

    ax.barh(range(n_mvps + 1, 1, -1), mvps_roi.roi, color="#f5c518", edgecolor="none")

    ax.set_yticks([])
    ax.spines["bottom"].set_linewidth(2)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.xaxis.grid(False)
    ax.xaxis.set_ticks_position("none")

    plt.suptitle("ROI > 30%", y=0.925)

    plt.xticks(fontsize=14)

    # Display movie names on bars
    for pos, name in tuple(zip(range(n_mvps + 1, 1, -1), mvps_roi.englishTitle)):
        ax.text(
            0.5,
            pos,
            name,
            va="center",
            ha="left",
            fontsize=18,
            fontweight="regular",
            color="#444",
        )

    return fig


def earning_graph():
    movies = pd.read_csv("EDA_data/movies.csv", sep=";")
    plt.style.use("dark_background")

    # Preparing data
    n_mvps = 10
    mvps_grossWorld = movies[["englishTitle", "grossWorld"]].sort_values(
        by="grossWorld", ascending=False
    )[:n_mvps]

    fig, ax = plt.subplots(figsize=(9, 6.5))

    ax.barh(
        range(n_mvps + 1, 1, -1),
        mvps_grossWorld.grossWorld,
        color="#f5c518",
        edgecolor="none",
    )

    ax.set_yticks([])
    ax.spines["bottom"].set_linewidth(2)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.xaxis.grid(False)

    plt.xlabel("Millions of Dollars", labelpad=15)

    # Cambibar el texto de los xticks
    fig.canvas.draw()
    labels = [item.get_text().replace(".", "") for item in ax.get_xticklabels()]
    labels[0] = 0
    labels[1] = 0
    labels = [int(item) * 100 for item in labels]
    labels = [
        "{:,.2f}".format(item).replace(".", "").replace(",", ".")[:-2]
        for item in labels
    ]

    ax.set_xticklabels(labels)
    ax.xaxis.set_ticks_position("none")

    plt.xticks(fontsize=14)

    # Display movie names on bars
    for pos, name in tuple(zip(range(n_mvps + 1, 1, -1), mvps_grossWorld.englishTitle)):
        ax.text(
            20000000,
            pos,
            name,
            va="center",
            ha="left",
            fontsize=16,
            fontweight="regular",
            color="#444",
        )

    return fig
