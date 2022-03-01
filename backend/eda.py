import ast
import datetime
import json

import chart_studio
import chart_studio.plotly as py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
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
