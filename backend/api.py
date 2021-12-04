from numpy.core.fromnumeric import mean
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances

movies = pd.read_csv("movies.csv",encoding="Latin1")
Ratings = pd.read_csv("ratings.csv")
Tags = pd.read_csv("tags.csv",encoding="Latin1")


Mean = Ratings.groupby(by="userId",as_index=False)['rating'].mean()
Rating_avg = pd.merge(Ratings,Mean,on='userId')
Rating_avg['adg_rating'] = Rating_avg['rating_x']-Rating_avg['rating_y']
Rating_avg.head()