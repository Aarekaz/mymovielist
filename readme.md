## Introduction

My Movie List is a movie recommendation system that recommends movies and tv shows
to the user based on their watch history and personal preferences. It recommends movies
and series based on collaborative filtering. The need for such a system is in demand due to
the increase in streaming services during the pandemic. In this age of digitized media, a
recommendation system that caters to a user’s preference is highly needed. The main aim
of the project is to provide a one-stop solution for the user's entertainment needs. The
project can serve recommendations to the user based on the user’s input as well as the user’s
past behavior and also is able to stream most of the recommendations.

### Thesis

View the project thesis [here](/documentations/My%20Movie%20List%20Report.pdf).



## Features

- Users are able to search and view details regarding any movie/show.
- Users are able to access the dashboard and see different visualizations.
- Movie recommendations are served to the user based on their liking and item ratings
  as well as ratings given by other users.
- Users are able to see links to where they can view the movie.
- Users are able to see visualizations based on different attributes of movies.

## Technologies Used

- ReactJS: It was used to create the frontend of our web application based on the
  Figma design.
- TMDb API: It was used to access the data required to display in the frontend of the
  application. The data called by the API ranged from names to cast lists, episode
  links as well as links to clips from YouTube.
- Python: It was used to create the recommendation engine as well as the dashboard
  for the user to interact on. It was also used to perform EDA on the dataset and build
  visualizations.

## How algorithm works

![Algorithm](/documentations/Images/knn.gif)
![Algorithm](/documentations/Images/knn_with_5_neighbors.gif)

## System Flow Chart

![System Flow Chart](/documentations/Images/system-flow.png)

## Algotithm

Item-based collaborative filtering and user-based collaborative filtering are being tested on the application. For the item-based collaborative filtering, the similarities between different items are calculated by using cosine similarity and clustered KNN algorithm. In the real world, ratings are very sparse and data points are mostly collected from very popular movies and highly engaged users. So we reduced the noise by adding some filters and qualified the movies for the final dataset.

- To qualify for a movie, a minimum of 10 users should have voted for a movie.
- To qualify a user, a minimum of 50 movies should have been voted by the user. 

Our final dataset has dimensions of  2121 * 378.
The similarity values between items are measured by observing all the users who have rated both the items. As shown in the diagram below, the similarity between two items is dependent upon the ratings given to the items by users who have rated both of them:

![Finding Similarity](/documentations/Images/finding_similarity.png)
![Item Based Collaborative Filtering](/documentations/Images/item_based_filterring.png)



## Screenshots

### Frontend

#### Home Page 
![Home Page](/documentations/Screenshots/homebanner.png)
![Home Page](/documentations/Screenshots/home2.png)

#### Show Details
![Show Details](/documentations/Screenshots/show_details.png)

### Recommendor
![Dashboard](/documentations/Screenshots/recommender_dashboard.png)

#### User Based Reccomendation
![User Based Reccomendation](/documentations/Screenshots/user_based_recommendation.png)

#### Item Based Reccomendation

![Item Based Reccomendation](/documentations/Screenshots/item_based_recomendation.png)


## Team Members

- [Apurba Shrestha]("https://www.linkedin.com/in/apurbashrestha/")
- [Prakriti Bista]("https://www.linkedin.com/in/itsmeprakriti/")
- [Siddhartha Shrestha]("https://www.linkedin.com/in/siddhartha-shrestha-2ba58a21b/")


