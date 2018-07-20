import requests
import pandas as pd
import time

url_base='https://api.themoviedb.org/3/movie/'
api_key = '?api_key=3379adc9490a8bde1f9b308c713620b3'

min_movie_id = 2
max_movie_id = 536681

def find_all_movies():
    movie_id = min_movie_id
    dict_list = []
    while movie_id <= 1250:
        if movie_id % 40 == 0:
            time.sleep(10)
        full_url = url_base+str(movie_id)+api_key
        json=requests.get(full_url).json()
        if "status_code" in json:
            movie_id+=1
        else:
            dict_list.append(dict(budget=json['budget'],revenue = json['revenue'],release_date = json['release_date'], tconst = json['imdb_id'],runtime = json['runtime'], movie_id= movie_id))
            movie_id+=1
        print(movie_id)
    return dict_list

list_of_movie_dicts = find_all_movies()

#convert list of dicts into dataframe
moviedb_df = pd.DataFrame(list_of_movie_dicts)

moviedb_df.to_csv('sample_moviedb_df.csv')
