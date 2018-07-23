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

######################  GENRES  ######################

genre_order = [gen.to_dict() for gen in Genre.query.order_by(Genre.name).all()]
#shows a count of how many genres had movies
def genre_count_layout():
    genres = [gen.name for gen in Genre.query.order_by(Genre.name).all()]
    genre_count = [Genre.query.filter(Genre.id == MovieGenre.genre_id).filter(Genre.name== type).count() for type in genres]
    return {'data' : [{
                 'x' : genres,
                 'y' : genre_count,
                 'name' : "Movie Genres",
                 'type' : 'bar'
                 }],
                 'layout' : {'title': "Total Genres Released"}
                 }

def movies_to_genre(genre):
    pay_movies = [movie for movie in Movie.query.filter(Movie.revenue >  0).all()]
    total = 0
    for pay in pay_movies:
        if pay.title in genre['movies']:
            total += pay.revenue
    tot =round(total)
    return '${:,}'.format(tot)

#Genre total made
def genre_total_layout():
    total = [movies_to_genre(g) for g in genre_order]
    x_values = [genre['name'] for genre in genre_order]
    y_values = total
    return  {'data' : [{
                 'x' : x_values,
                 'y' : y_values,
                 'name' : "Movie Genres",
                 'type' : 'bar',
                 'color' : "green"
                 }],
                 'layout' :{'title': "Total Amount made for each Genre"}
                 }

def genre_avg(genre):
    pay_movies = [movie for movie in Movie.query.filter(Movie.revenue >  0).all()]
    total = 0
    amt = 0
    for pay in pay_movies:
        if pay.title in genre['movies']:
            total += pay.revenue
            amt+=1
    full_avg = round(total/amt)
    return '${:,}'.format(full_avg)

def genre_avg_layout():
    total = [genre_avg(g) for g in genre_order]
    x_values = [genre['name'] for genre in genre_order]
    y_values = total
    return {'data' : [{
                 'x' : x_values,
                 'y' : y_values,
                 'name' : "Movie Genres",
                 'type' : 'bar',
                 'color' : 'red'
                 }],
                 'layout' : {'title': "Average Amount Made for each Genre"}
                 }

def genre_setup():
    return [{'label': gen['name'], 'value': gen['id']} for gen in genre_order]

def movie_to_month_with_genre(month, genre):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_month = [movie for movie in all_movies_dict if int(movie['release_date'][5:7]) == month]
    movies_w_genre = [gen for gen in movies_in_month if (genre[0] in gen['genres'])]
    return movies_w_genre

#how many a month
def get_trace(genre):
    picked_genre = [gen['name'] for gen in genre_order if gen['id'] == genre]
    gen_and_month = [movie_to_month_with_genre(month, picked_genre) for month in months]
    genre_month_hist = [len(x) for x in gen_and_month]
#    pdb.set_trace()
    return {
         'x' : [calendar.month_name[i]for i in months],
         'y' : genre_month_hist,
         'name' : picked_genre[0],
         'type' : 'line'
         }
def genre_months(genre):
    traces = [get_trace(g) for g in genre]
    # pdb.set_trace()
    return dcc.Graph(
            id = "Genres_per_month",
            figure ={'data' :
                traces,
                 'layout' : {'title': "Movies in Genre per month"}
                 })

#how much made a month
def month_genre_made(month, genre):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_month = [movie for movie in all_movies_dict if int(movie['release_date'][5:7]) == month]
    movies_w_genre = [gen for gen in movies_in_month if (genre[0] in gen['genres'])]
    move_rev = [r['revenue'] for r in movies_w_genre]
    return sum(move_rev)

def get_tot_trace(genre):
    picked_genre = [gen['name'] for gen in genre_order if gen['id'] == genre]
    gen_and_month = [month_genre_made(month, picked_genre) for month in months]
    return { 'x' : [calendar.month_name[i]for i in months],
             'y' : gen_and_month,
             'name' : picked_genre[0],
             'type' : 'line'
             }
def genre_tot_months(genre):
    traces = [get_tot_trace(g) for g in genre]
    return dcc.Graph(
            id = "Genres_per_month",
            figure ={'data' :
                traces,
                 'layout' : {'title': "Genre Total $ made per month"}
                 })

#how much profit a month
def month_profit_made(month, genre):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_month = [movie for movie in all_movies_dict if int(movie['release_date'][5:7]) == month]
    movies_w_genre = [gen for gen in movies_in_month if (genre[0] in gen['genres'])]
    move_rev = [(r['revenue'] - r['budget']) for r in movies_w_genre]
    return sum(move_rev)

def get_pro_trace(genre):
    picked_genre = [gen['name'] for gen in genre_order if gen['id'] == genre]
    gen_and_month = [month_profit_made(month, picked_genre) for month in months]
    return { 'x' : [calendar.month_name[i]for i in months],
             'y' : gen_and_month,
             'name' : picked_genre[0],
             'type' : 'line'
             }
def genre_profits_months(genre):
    traces = [get_pro_trace(g) for g in genre]
    return dcc.Graph(
            id = "Genres_per_month",
            figure ={'data' :
                traces,
                 'layout' : {'title': "Genre Profit per month"}
                 })
