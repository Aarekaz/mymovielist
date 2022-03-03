import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from functions import *

movies = pd.read_csv("data/movies.csv", encoding="latin-1")
ratings = pd.read_csv("data/ratings.csv", encoding="latin-1")

final_dataset = ratings.pivot(index="movieId", columns="userId", values="rating")
final_dataset.fillna(0, inplace=True)

no_user_voted = ratings.groupby("movieId")["rating"].agg("count")
no_movies_voted = ratings.groupby("userId")["rating"].agg("count")

final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index, :]
final_dataset = final_dataset.loc[:, no_movies_voted[no_movies_voted > 50].index]
sample = np.array([[0, 0, 3, 0, 0], [4, 0, 0, 0, 2], [0, 0, 0, 0, 1]])
sparsity = 1.0 - (np.count_nonzero(sample) / float(sample.size))

csr_sample = csr_matrix(sample)

csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)
knn = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=20, n_jobs=-1)
knn.fit(csr_data)


def get_movie_recommendation(movie_name: str, n):
    n_movies_to_reccomend = n
    movie_list = movies[movies["title"].str.contains(movie_name)]
    if len(movie_list):
        movie_idx = movie_list.iloc[0]["movieId"]
        movie_idx = final_dataset[final_dataset["movieId"] == movie_idx].index[0]

        distances, indices = knn.kneighbors(
            csr_data[movie_idx], n_neighbors=n_movies_to_reccomend + 1
        )
        rec_movie_indices = sorted(
            list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
            key=lambda x: x[1],
        )[:0:-1]

        recommend_frame = []

        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]["movieId"]
            idx = movies[movies["movieId"] == movie_idx].index
            recommend_frame.append(
                {
                    "Title": movies.iloc[idx]["title"].values[0],
                    "Genre": movies.iloc[idx]["genres"].values[0],
                    "Distance": val[1],
                }
            )
        df = pd.DataFrame(recommend_frame, index=range(1, n_movies_to_reccomend + 1))

        # (index|columns|records|split|table)
        js = df.to_json(orient="index")

        final_list = list()
        for row in df.iterrows():
            final_list.append(row[1].to_dict())

        with open("notebooks\json_data\data.json", "w") as f:
            f.write(json.dumps(final_list, indent=4))

        # with open('json_data/data.json', 'w', encoding='utf-8') as f:
        #     json.dump(js, f, ensure_ascii=False, indent=4)
        print(json.dumps(final_list, indent=4))
        st.write("The ", n, "movies recommended to you similar to", movie_name, "are:")
        movie_bar(n)
        return st.dataframe(df)

    else:
        return st.error("Opps! No movies found. Please check your input")
