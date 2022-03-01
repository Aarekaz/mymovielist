from email import header
import requests
import pprint
import pandas as pd

api_key = "40f84ea0b622bc4257dabf9631a401dc"
api_keyv4 = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI0MGY4NGVhMGI2MjJiYzQyNTdkYWJmOTYzMWE0MDFkYyIsInN1YiI6IjYxYTAzMTgwZDEzMzI0MDA2MmE1OTNmZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.P6ceISSm91gPLodb_ncPh9eRWOTyOcj_vDRLo5OYavM"

#API version3
movie_id = 500
api_version = 3
api_base_url = f"https://api.themoviedb.org/{api_version}"
endpoint_path = f"/movie/{movie_id}"
endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}"
pprint.pprint(endpoint)
# r=requests.get(endpoint)
# print(r.status_code)
# print(r.text)

#API version4
#is incomplete!! 
#let's not use this.
movie_id = 501
api_version = 4
api_base_url = f"https://api.themoviedb.org/{api_version}"
endpoint_path = f"/movie/{movie_id}"
endpoint = f"{api_base_url}{endpoint_path}"
headers = {
    'Authorization': f'Bearer {api_keyv4}',
    'Content-Type': 'application/json;charset=utf-8'
}
# r = requests.get(endpoint,headers = headers)
# print(r.status_code)
# print(r.text)


api_base_url = f"https://api.themoviedb.org/{api_version}"
endpoint_search = f"/search/movie"
# endpoint_movieImage = f"/movie/{movie_id}/images"

search_query = "The Matrix"
endpoint = f"{api_base_url}{endpoint_search}?api_key={api_key}&query={search_query}"
# images = f"{api_base_url}{endpoint_movieImage}?api_key={api_key}"
# print(endpoint)
r=requests.get(endpoint)
# pprint.pprint(r.json())

if r.status_code in range(200,299):
    data = r.json()
    results = data['results']
    if len(results)>0:
        # print(results[0].keys())   
        movie_ids= set()
        for result in results:
            _id = result['id']
            # print(result['title'],_id)
            movie_ids.add(_id)
        # print(list(movie_ids)) 
output= 'movies.csv'
movie_data = []
for movie_id in movie_ids:
    api_version = 3
    api_base_url = f"https://api.themoviedb.org/{api_version}"
    endpoint_path = f"/movie/{movie_id}"
    endpoint = f"{api_base_url}{endpoint_path}?api_key={api_key}"
    r = requests.get(endpoint)
    if r.status_code in range(200,299):
        data = r.json()
        movie_data.append(data)


df = pd.DataFrame(movie_data)
print(df.head())
df.to_csv(output,index=False)


