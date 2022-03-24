from random import randrange
from turtle import end_poly, pos
from unittest import result
import requests
import pprint
import streamlit as st


api_key = "40f84ea0b622bc4257dabf9631a401dc"
api_version = 3
api_base_url = f"https://api.themoviedb.org/{api_version}"
endpoint_path ="/movie/popular"
endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}&language=en-US&page=1"

# endpoint = "https://api.themoviedb.org/3/movie/popular?api_key=40f84ea0b622bc4257dabf9631a401dc&language=en-US&page=1"
r = requests.get(endpoint)
pprint.pprint(r.json())
poster = []
id = []
if r.status_code in range(200,299):
    data  = r.json()
    results = data['results']
    movie_ids = set()
    for result in results:
        poster_path = result['poster_path']
        movie_id = result['id']
        full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
        id.append(movie_id)
        poster.append(full_path)
        firstTenPoster = poster[0:10]
        firstTenId = id[0:10]

def LinkToFrontend():
    front_end = f"http://localhost:3000/movie/"

    ncol = 10
    wcol = 10

    cols = st.columns(ncol)

    for i in range(ncol):
        col = cols[i % wcol]
        # col.image(df_f['tmdbId'][i],use_column_width = "always")

        # {front_end}{tmdb_id}

        poster_link = f"{firstTenPoster[i]}"
        tmdb_id = f"{firstTenId[i]}"

        with col:
            # st.markdown(f"[![Foo]({poster_link})]({front_end}+{tmdb_id})")
            st.markdown(f'''
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
                unsafe_allow_html=True
            )
            
