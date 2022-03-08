import warnings
from ast import literal_eval

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from nltk.corpus import wordnet
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from scipy import stats
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel
from surprise import SVD, Dataset, Reader
from surprise.model_selection import cross_validate

warnings.simplefilter("ignore")


def convert_int(x):
    try:
        return int(x)
    except:
        return np.nan


md = pd.read_csv("../EDA_data/movies_metadata.csv")
md["genres"] = (
    md["genres"]
    .fillna("[]")
    .apply(literal_eval)
    .apply(lambda x: [i["name"] for i in x] if isinstance(x, list) else [])
)

links_small = pd.read_csv("../EDA_data/links_small.csv")
links_small = links_small[links_small["tmdbId"].notnull()]["tmdbId"].astype("int")
smd = md[md["id"].isin(links_small)]

id_map = pd.read_csv("../EDA_data/links_small.csv")[["movieId", "tmdbId"]]
id_map["tmdbId"] = id_map["tmdbId"].apply(convert_int)
id_map.columns = ["movieId", "id"]
id_map = id_map.merge(smd[["title", "id"]], on="id").set_index("title")


indices = pd.Series(smd.index, index=smd["title"])


count = CountVectorizer(
    analyzer="word", ngram_range=(1, 2), min_df=0, stop_words="english"
)
count_matrix = count.fit_transform(smd["soup"])

cosine_sim = cosine_similarity(count_matrix, count_matrix)
svd = SVD()
indices_map = id_map.set_index('id')

def hybrid(userId, title):
    idx = indices[title]
    tmdbId = id_map.loc[title]["id"]
    # print(idx)
    movie_id = id_map.loc[title]["movieId"]

    sim_scores = list(enumerate(cosine_sim[int(idx)]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]

    movies = smd.iloc[movie_indices][
        ["title", "vote_count", "vote_average", "year", "id"]
    ]
    movies["est"] = movies["id"].apply(
        lambda x: svd.predict(userId, indices_map.loc[x]["movieId"]).est
    )
    movies = movies.sort_values("est", ascending=False)
    return movies.head(10)
