import json
from turtle import pos

import numpy as np
import pandas as pd
import requests
import streamlit as st
from sklearn.metrics import pairwise_distances
from sklearn.metrics.pairwise import cosine_similarity

movies = pd.read_csv("data/movies.csv", encoding="Latin1")
Ratings = pd.read_csv("data/ratings.csv")
Tags = pd.read_csv("data/tags.csv", encoding="Latin1")
links = pd.read_csv("data/links.csv", header=0, delim_whitespace=False)

Mean = Ratings.groupby(by="userId", as_index=False)["rating"].mean()
Rating_avg = pd.merge(Ratings, Mean, on="userId")
Rating_avg["adg_rating"] = Rating_avg["rating_x"] - Rating_avg["rating_y"]

check = pd.pivot_table(Rating_avg, values="rating_x", index="userId", columns="movieId")
final = pd.pivot_table(
    Rating_avg, values="adg_rating", index="userId", columns="movieId"
)

# data cleaning
# Replacing NaN by Movie Average
final_movie = final.fillna(final.mean(axis=0))

# Replacing NaN by user Average
final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)


# user similarity on replacing NaN by user avg
b = cosine_similarity(final_user)
np.fill_diagonal(b, 0)
similarity_with_user = pd.DataFrame(b, index=final_user.index)
similarity_with_user.columns = final_user.index

# user similarity on replacing NaN by item(movie) avg
cosine = cosine_similarity(final_movie)
np.fill_diagonal(cosine, 0)
similarity_with_movie = pd.DataFrame(cosine, index=final_movie.index)
similarity_with_movie.columns = final_user.index


def find_n_neighbours(df, n):
    order = np.argsort(df.values, axis=1)[:, :n]
    df = df.apply(
        lambda x: pd.Series(
            x.sort_values(ascending=False).iloc[:n].index,
            index=["top{}".format(i) for i in range(1, n + 1)],
        ),
        axis=1,
    )
    return df


# top 30 neighbours for each user
sim_user_30_u = find_n_neighbours(similarity_with_user, 30)

# top 30 neighbours for each Movie
sim_user_30_m = find_n_neighbours(similarity_with_movie, 30)


def get_user_similar_movies(user1, user2):
    common_movies = Rating_avg[Rating_avg.userId == user1].merge(
        Rating_avg[Rating_avg.userId == user2], on="movieId", how="inner"
    )
    return common_movies.merge(movies, on="movieId")


Rating_avg = Rating_avg.astype({"movieId": str})
Movie_user = Rating_avg.groupby(by="userId")["movieId"].apply(lambda x: ",".join(x))

poster = []
api_key = "40f84ea0b622bc4257dabf9631a401dc"
api_version = 3
api_base_url = f"https://api.themoviedb.org/{api_version}"


def user_recomender(user, n):
    # user = int(user)
    poster.clear()
    global df_f
    Movie_seen_by_user = check.columns[
        check[check.index == user].notna().any()
    ].tolist()
    a = sim_user_30_m[sim_user_30_m.index == user].values
    b = a.squeeze().tolist()
    d = Movie_user[Movie_user.index.isin(b)]
    l = ",".join(d.values)
    Movie_seen_by_similar_users = l.split(",")
    Movies_under_consideration = list(
        set(Movie_seen_by_similar_users) - set(list(map(str, Movie_seen_by_user)))
    )
    Movies_under_consideration = list(map(int, Movies_under_consideration))
    score = []
    for item in Movies_under_consideration:
        c = final_movie.loc[:, item]
        d = c[c.index.isin(b)]
        f = d[d.notnull()]
        avg_user = Mean.loc[Mean["userId"] == user, "rating"].values[0]
        index = f.index.values.squeeze().tolist()
        corr = similarity_with_movie.loc[user, index]
        fin = pd.concat([f, corr], axis=1)
        fin.columns = ["adg_score", "correlation"]
        fin["score"] = fin.apply(lambda x: x["adg_score"] * x["correlation"], axis=1)
        nume = fin["score"].sum()
        deno = fin["correlation"].sum()
        final_score = avg_user + (nume / deno)
        score.append(final_score)
    data = pd.DataFrame({"movieId": Movies_under_consideration, "score": score})
    top_recommendation = data.sort_values(by="score", ascending=False).head(n)
    Movie_Name = top_recommendation.merge(movies, how="inner", on="movieId")
    new_df = links.loc[links["movieId"].isin(Movie_Name["movieId"])]
    df_f = pd.merge(Movie_Name, new_df)

    for movie_id in df_f["tmdbId"]:
        endpoint_path = f"/movie/{movie_id}"
        endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}&language=en-US"
        data = requests.get(endpoint)
        data = data.json()
        poster_path = data["poster_path"]
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        poster.append(full_path)

    df_f["Poster"] = poster

    # js = df_f.to_json(orient="index")

    final_list = list()
    for row in df_f.iterrows():
        final_list.append(row[1].to_dict())

    with open("notebooks\json_data\data_user.json", "w") as f:
        f.write(json.dumps(final_list, indent=4))

    # with open('json_data/data.json', 'w', encoding='utf-8') as f:
    #     json.dump(js, f, ensure_ascii=False, indent=4)
    print(json.dumps(final_list, indent=4))
    st.write("The ", n, "movies recommended to you similar to", user, "are:")

    # Movie_Names = Movie_Name.title.values.tolist()
    return movie_bar(n)


def movie_bar(n):
    front_end = f"http://localhost:3000/movie/"

    ncol = n
    wcol = 4

    cols = st.columns(ncol)

    for i in range(ncol):
        col = cols[i % wcol]
        # col.image(df_f['tmdbId'][i],use_column_width = "always")

        # {front_end}{tmdb_id}

        poster_link = f"{df_f['Poster'][i]}"
        tmdb_id = f"{df_f['tmdbId'][i]}"

        with col:
            # st.markdown(f"[![Foo]({poster_link})]({front_end}+{tmdb_id})")
            st.markdown(
                f'''
                    <style>
                        img{"""{
                            width: 100%;
                            height: auto;
                            max-width: 50vw;
                            }
                            """
                        }
                    </style>
                    <a href="{front_end}{tmdb_id}">
                        <img src="{poster_link}"/>
                    </a>
                ''',
                unsafe_allow_html=True,
            )
