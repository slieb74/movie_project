import pandas as pd
import os
from models import Movie, Director, Genre, MovieGenre, db

cwd = os.getcwd()

imdb_table = pd.read_csv(cwd+'/combined_imdb_tables.csv', index_col=0, low_memory=False)

data = imdb_table.to_dict('records')[1:]

df = pd.DataFrame(data)

mask = (df['directors'] != '\\N') & (df['runtimeMinutes'] != '\\N') & (df['genres'] != '\\N') & (df['numVotes'] > 1000)

clean_df = df[mask]#.drop(columns='titleType')

#import moviedb_table
moviedb_table = pd.read_csv(cwd+'/sample_moviedb_df.csv', index_col=0, low_memory=False)

#merge tables
joined_table = pd.merge(clean_df,moviedb_table, on='tconst')

#clean joined_table
joined_table = joined_table.drop(columns=['runtimeMinutes', 'titleType', 'startYear', 'numVotes', 'movie_id'])

#remove all secondary directors
def remove_extra_directors():
    c=0
    while c < len(joined_table):
        joined_table['directors'][c] = joined_table['directors'][c].split(',')[0]
        c+=1
    return joined_table

joined_table=remove_extra_directors()

#turn joined_table into dict
data = joined_table.to_dict('records')

def create_director_objects(data):
    directors_list = []
    director_objects = []
    for row in data:
        directors_list.append(row['directors'])#.split(',')
    directors_list = list(set(directors_list))
    for director in directors_list:
        director_objects.append(Director(name=director))
    return director_objects

def create_genre_objects(data):
    genres_list = []
    genre_objects = []
    for row in data:
        g = row['genres'].split(',')
        genres_list.extend(g)
    genres_list = list(set(genres_list))
    for genre in genres_list:
        genre_objects.append(Genre(name=genre))
    return genre_objects

def create_movie_object(data):
    movie_objects = []
    directors = Director.query.all()
    genres = Genre.query.all()
    for row in data:
        split_genres = row['genres'].split(',')
        for d in directors:
            if row['directors']== d.name:
                movie = (Movie(title=row['primaryTitle'], budget=row['budget'], revenue=row['revenue'], release_date=row['release_date'], runtime=row['runtime'], imdb_rating=row['averageRating'], director=d))
                for genre in genres:
                    for g in split_genres:
                        if g == genre.name:
                            movie.genres.append(genre)
                movie_objects.append(movie)
    return movie_objects

def main_function():
    director_list = create_director_objects(data)
    db.session.add_all(director_list)
    db.session.commit()

    genre_list = create_genre_objects(data)
    db.session.add_all(genre_list)
    db.session.commit()

    movie_list = create_movie_object(data)
    db.session.add_all(movie_list)
    db.session.commit()
