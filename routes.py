from flask import render_template, jsonify, json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_sqlalchemy import SQLAlchemy
from __init__ import app
from models import Movie, Director, Genre, MovieGenre
import dashboard

@app.server.route('/movies')
def movies():
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()][0]
    return jsonify(all_movies_dict)

@app.server.route('/movies/year/<int:year>')
def movies_by_year(year):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_year = [movie for movie in all_movies_dict if int(movie['release_date'][:4]) == year]
    return jsonify(movies_in_year)

# @app.server.route('/tweets')
# def tweets_index():
#     all_tweets = Tweet.query.all()
#     all_tweets_dicts = [tweet.to_dict() for tweet in all_tweets]
#     return render_template('tweets.html', tweets=all_tweets_dicts)

@app.server.route('/directors')
def directors():
    all_directors_dict = [director.to_dict() for director in Director.query.all()][0]
    return jsonify(all_directors_dict)

@app.server.route('/genres')
def genres():
    all_genres_dict = [genre.to_dict() for genre in Genre.query.all()][0]
    return jsonify(all_genres_dict)
