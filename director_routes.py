from flask import render_template, jsonify, json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_sqlalchemy import SQLAlchemy
from __init__ import app
from models import Movie, Director, Genre, MovieGenre
import calendar
import plotly.graph_objs as go
from movie_routes import *

season_dict={'summer':['06','07','08'], 'fall':['09','10','11'], 'winter':['12','01','02'], 'spring':['03','04','05']}
months = [1,2,3,4,5,6,7,8,9,10,11,12]

##################### DIRECTORS ##########################
def director_count():
    directors = [director.name for director in Director.query.all()]
    movies = [len(director.movies) for director in Director.query.all()]
    return dcc.Graph(
            id='directors-count',
            figure ={'data': [
                    {'x': directors, 'y': movies, 'type': 'bar'}],
                'layout': {
                    'title': 'Director Count',
                    'xaxis': {'title': 'Director ID'},
                    'yaxis': {'title': 'Number of Movies'},
                    'margin': {'b': 120},
        }})

def avg_revenue_by_director(director):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_by_director = [movie for movie in all_movies_dict if movie['director']==director and movie['revenue']>0]
    sum_revenue = sum([movie['revenue'] for movie in movies_by_director])
    avg_revenue = round(sum_revenue/len(movies_by_director))
    return avg_revenue

def director_revenue_graph():
    movie_info = movie_info_tuples()
    directors = [info[4] for info in movie_info]
    return dcc.Graph(
        id='bar-graph-avg_rev_directors',
        figure ={'data': [
                {'x': directors, 'y': [avg_revenue_by_director(director) for director in directors], 'type': 'bar'}],
            'layout': {
                'title': 'Average Revenue for Director',
                'xaxis': {'title': 'Director'},
                'yaxis': {'title': 'Revenue'},
                'margin': {'b': 120},
    }})
