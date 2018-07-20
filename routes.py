from flask import render_template, jsonify, json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_sqlalchemy import SQLAlchemy
from __init__ import app
from models import Movie, Director, Genre, MovieGenre
import dashboard
import calendar

season_dict={'summer':['06','07','08'], 'fall':['09','10','11'], 'winter':['12','01','02'], 'spring':['03','04','05']}

@app.server.route('/movies')
def movies():
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    return render_template('movies.html',movies=all_movies_dict)

@app.server.route('/movies/<int:id>')
def movie_by_id(id):
    movie = Movie.query.filter(Movie.id == id).first()
    return render_template('movie_show.html',movie=movie.to_dict())

@app.server.route('/movies/year/<int:year>')
def movies_by_year(year):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_year = [movie for movie in all_movies_dict if int(movie['release_date'][:4]) == year]
    return render_template('movies.html',movies=movies_in_year)

@app.server.route('/movies/year/<int:year>/<int:month>')
def movies_by_year_and_month(year, month):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_year_and_month = [movie for movie in all_movies_dict if int(movie['release_date'][:4]) == year and int(movie['release_date'][5:7]) == month ]
    return render_template('movies.html',movies=movies_in_year_and_month)

@app.server.route('/movies/year/<int:start_year>-<int:end_year>')
def movies_by_year_range_inclusive(start_year, end_year):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_year_range = [movie for movie in all_movies_dict if (start_year <= int(movie['release_date'][:4]) <= end_year)]
    return render_template('movies.html',movies=movies_in_year_range)

@app.server.route('/movies/month/<int:month>')
def movies_by_month(month):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_month = [movie for movie in all_movies_dict if int(movie['release_date'][5:7]) == month]
    return render_template('movies.html',movies=movies_in_month)

@app.server.route('/movies/month/<int:month>/revenue')
def avg_revenue_by_month(month):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_month = [movie for movie in all_movies_dict if int(movie['release_date'][5:7]) == month]
    #remove movies where revenue = 0
    movies_excl_zero_revenue = [movie for movie in movies_in_month if movie['revenue'] > 0]
    sum_revenue = sum([movie['revenue']for movie in movies_excl_zero_revenue])
    avg_revenue = round(sum_revenue/len(movies_excl_zero_revenue))
    return render_template('revenue_show.html',timeframe=calendar.month_name[month],avg_revenue=' ${:,}'.format(avg_revenue),movies=movies_excl_zero_revenue)

@app.server.route('/movies/season/<season>')
def movies_by_season(season):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_season = [movie for movie in all_movies_dict if movie['release_date'][5:7] in season_dict.get(season)]
    return render_template('movies.html',movies=movies_in_season)

@app.server.route('/movies/season/<season>/revenue')
def avg_revenue_by_season(season):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_season = [movie for movie in all_movies_dict if movie['release_date'][5:7] in season_dict.get(season)]
    #remove movies where revenue = 0
    movies_excl_zero_revenue = [movie for movie in movies_in_season if movie['revenue'] > 0]
    sum_revenue = sum([movie['revenue']for movie in movies_excl_zero_revenue])
    avg_revenue = round(sum_revenue/len(movies_excl_zero_revenue))
    return render_template('revenue_show.html',timeframe=season,avg_revenue=' ${:,}'.format(avg_revenue),movies=movies_excl_zero_revenue)

@app.server.route('/movies/max/budget/<int:budget>')
def movies_by_max_budget(budget):
    movies_with_max_budget = [movie.to_dict() for movie in Movie.query.all() if movie.budget <= budget]
    return render_template('movies.html',movies=movies_with_max_budget)

@app.server.route('/movies/min/budget/<int:budget>')
def movies_with_min_budget(budget):
    movies_with_min_budget = [movie.to_dict() for movie in Movie.query.all() if movie.budget >= budget]
    return render_template('movies.html',movies=movies_with_min_budget)

@app.server.route('/movies/max/revenue/<int:revenue>')
def movies_with_max_revenue(revenue):
    movies_with_max_revenue = [movie.to_dict() for movie in Movie.query.all() if movie.revenue <= revenue]
    return render_template('movies.html',movies=movies_with_max_revenue)

@app.server.route('/movies/min/revenue/<int:revenue>')
def movies_with_min_revenue(revenue):
    movies_with_min_revenue = [movie.to_dict() for movie in Movie.query.all() if movie.revenue >= revenue]
    return render_template('movies.html',movies=movies_with_min_revenue)

@app.server.route('/movies/min/runtime/<int:runtime>')
def movies_by_min_runtime(runtime):
    movies_with_min_runtime = [movie.to_dict() for movie in Movie.query.all() if movie.runtime >= runtime]
    return render_template('movies.html',movies=movies_with_min_runtime)

@app.server.route('/movies/max/runtime/<int:runtime>')
def movies_by_max_runtime(runtime):
    movies_with_max_runtime = [movie.to_dict() for movie in Movie.query.all() if movie.runtime <= runtime]
    return render_template('movies.html',movies=movies_with_max_runtime)

@app.server.route('/movies/max/imdb/<float:rating>')
def movies_with_max_imdb_rating(rating):
    movies_with_max_rating = [movie.to_dict() for movie in Movie.query.all() if float(movie.imdb_rating) <= rating]
    return render_template('movies.html',movies=movies_with_max_rating)

@app.server.route('/movies/min/imdb/<float:rating>')
def movies_with_min_imdb_rating(rating):
    movies_with_min_rating = [movie.to_dict() for movie in Movie.query.all() if float(movie.imdb_rating) >= rating]
    return render_template('movies.html',movies=movies_with_min_rating)

@app.server.route('/movies/imdb/<float:min_rating>-<float:max_rating>')
def movies_by_imdb_rating_range(min_rating,max_rating):
    movies_within_range = [movie.to_dict() for movie in Movie.query.all() if min_rating <= float(movie.imdb_rating) <= max_rating]
    return render_template('movies.html',movies=movies_within_range)

@app.server.route('/movies/genres/<genre>')
def movies_by_genre(genre):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_by_genre = [movie for movie in all_movies_dict if genre.title() in movie['genres']]
    return render_template('movies.html',movies=movies_by_genre)

@app.server.route('/movies/genres/<genre1>-<genre2>')
def movies_by_genres(genre1,genre2):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_by_genre = [movie for movie in all_movies_dict if genre1.title() in movie['genres'] and genre2.title() in movie['genres']]
    return render_template('movies.html',movies=movies_by_genre)

@app.server.route('/movies/directors/<director>')
def movies_by_director(director):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_by_director = [movie for movie in all_movies_dict if director== movie['director']]
    return render_template('movies.html',movies=movies_by_director)

# @app.server.route('/directors')
# def directors():
#     all_directors_dict = [director.to_dict() for director in Director.query.all()][0]
#     return jsonify(all_directors_dict)
#
# @app.server.route('/genres')
# def genres():
#     all_genres_dict = [genre.to_dict() for genre in Genre.query.all()][0]
#     return jsonify(all_genres_dict)

@app.server.route('/genres')
def genres():
    all_genres_dict = [gen.name for gen in Genre.query.order_by(Genre.name).all()]
    return render_template('genres.html', genres = all_genres_dict)

@app.server.route('/genres/<genre>')
def specific_genre(genre):
    all_genre = [genre.to_dict() for genre in Genre.query.all()]
    guest_genre = [g['movies'] for g in all_genre if g['name']==genre.title()][0]
    return render_template('genre_show.html', genre=genre, movies=guest_genre)
    # return "<h1>Sorry, that is not a valid genre, please try another</h1>"
#Genre.query.filter(Genre.id== 1).first().movies

@app.server.route('/directors')
def directors():
    all_directors_dict = [dir.name for dir in Director.query.order_by(Director.name).all()]
    return render_template('directors.html', directors = all_directors_dict)

@app.server.route('/directors/<director>')
def choosen_director(director):
    all_direct = [direct.to_dict() for direct in Director.query.all()]
    guest_direct = [d['movies'] for d in all_direct if d['name']==director][0]
    return render_template('director_show.html', director=director, movies=guest_direct)
