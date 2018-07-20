import pandas as pd
import os
from models import Movie, Director, Genre, MovieGenre, db

cwd = os.getcwd()

imdb_table = pd.read_csv(cwd+'/combined_imdb_tables.csv', index_col=0, low_memory=False)

data = imdb_table.to_dict('records')[1:]

df = pd.DataFrame(data)

mask = (df['directors'] != '\\N') & (df['runtimeMinutes'] != '\\N') & (df['genres'] != '\\N') & (df['numVotes'] > 1000)

clean_df = df[mask].drop(columns='titleType')

#import moviedb_table
moviedb_table = pd.read_csv(cwd+'/sample_moviedb_df.csv', index_col=0, low_memory=False)

#merge tables
joined_table = pd.merge(clean_df,moviedb_table, on='tconst')

#clean joined_table
joined_table = joined_table.drop(columns=['runtimeMinutes', 'startYear', 'numVotes', 'movie_id'])

# #remove all secondary directors
def remove_extra_directors():
    c=0
    while c < len(joined_table):
        joined_table['directors'][c] = joined_table['directors'][c].split(',')[0]
        c+=1
    return joined_table

joined_table=remove_extra_directors()

#turn joined_table into dict
data = joined_table.to_dict('records')


def get_all_movies_and_genres(data=data):
    list_of_movie_and_genres = []
    for row in data:
        g_list = row['genres'].split(',')
        for g in g_list:
            obj = {'movie': row, 'genre':g}
            if obj not in list_of_movie_and_genres:
                list_of_movie_and_genres.append(obj)
    return list_of_movie_and_genres

def make_director(mg_obj):
    if Director.query.filter(Director.name==mg_obj['directors']).all():
        return Director.query.filter(Director.name==mg_obj['directors']).first()
    else:
        return Director(name=mg_obj['directors'])

def make_movie(mg_obj, director):
    if Movie.query.filter(Movie.title==mg_obj['primaryTitle']).first():
        return Movie.query.filter(Movie.title==mg_obj['primaryTitle']).first()
    else:
        return Movie(title=mg_obj['primaryTitle'], budget=mg_obj['budget'], revenue=mg_obj['revenue'], release_date=mg_obj['release_date'], runtime=mg_obj['runtime'], imdb_rating=mg_obj['averageRating'], director=director)

def make_genre(mg_obj):
    if Genre.query.filter(Genre.name==mg_obj).first():
        return Genre.query.filter(Genre.name==mg_obj).first()
    else:
        return Genre(name=mg_obj)

def all_instances(data):
    for movie_genre_obj in get_all_movies_and_genres():
        director = make_director(movie_genre_obj['movie'])
        movie = make_movie(movie_genre_obj['movie'], director)
        genre = make_genre(movie_genre_obj['genre'])
        movie_genre = MovieGenre(movie_id=movie.id,genre_id=genre.id)
        stuff_to_add = [movie, director, genre, movie_genre]
        db.session.add_all(stuff_to_add)
    db.session.commit()
