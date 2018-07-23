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

season_dict={'summer':['06','07','08'], 'fall':['09','10','11'], 'winter':['12','01','02'], 'spring':['03','04','05']}
months = [1,2,3,4,5,6,7,8,9,10,11,12]

######################  MOVIES  ######################
def movies_by_month(month):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_month = [movie for movie in all_movies_dict if int(movie['release_date'][5:7]) == month]
    return movies_in_month

def movie_count_by_month_graph():
    movies_in_month = [movies_by_month(month) for month in months]
    movies = [len(movies) for movies in movies_in_month]
    return dcc.Graph(
        id='bar-graph-movies-in-month',
        figure ={'data': [
                {'x': [calendar.month_name[month] for month in months], 'y': movies, 'type': 'bar'}],
            'layout': {
                'title': 'Movies Released by Month'
    }})

def avg_revenue_by_month(month):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_month = [movie for movie in all_movies_dict if int(movie['release_date'][5:7]) == month]
    movies_excl_zero_revenue = [movie for movie in movies_in_month if movie['revenue'] > 0]
    sum_revenue = sum([movie['revenue']for movie in movies_excl_zero_revenue])
    avg_revenue = round(sum_revenue/len(movies_excl_zero_revenue))
    return '${:,}'.format(avg_revenue)

def avg_revenue_month_graph():
    avg_revenue = [avg_revenue_by_month(month) for month in months]
    return dcc.Graph(
            id='bar-graph-avg-rev-months',
            figure={'data': [
                    {'x': [calendar.month_name[month] for month in months], 'y': avg_revenue, 'type': 'bar'},
                    {'x': [calendar.month_name[month] for month in months], 'y': avg_revenue, 'type': 'lines'}],
                'layout': {
                    'title': 'Average Revenue by Release Month',
                    'showlegend': False
    }})

def avg_revenue_by_season(season):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_season = [movie for movie in all_movies_dict if movie['release_date'][5:7] in season_dict.get(season)]
    movies_excl_zero_revenue = [movie for movie in movies_in_season if movie['revenue'] > 0]
    sum_revenue = sum([movie['revenue']for movie in movies_excl_zero_revenue])
    avg_revenue = round(sum_revenue/len(movies_excl_zero_revenue))
    #return '${:,}'.format(avg_revenue)
    return avg_revenue

def avg_revenue_season_graph():
    seasons=['summer', 'fall', 'winter', 'spring']
    avg_revenue = [avg_revenue_by_season(season) for season in seasons]
    return dcc.Graph(
            id='pie-graph-avg-rev-seasons',
            figure= {
                'data': [
                   go.Pie(
                        labels=seasons, values=avg_revenue, hoverinfo='label+percent+value')
                        ],
                'layout': go.Layout(
                    title='Average Revenue by Season Released')
                    })

def movie_info_tuples():
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_with_budget_and_rev = [movie for movie in all_movies_dict if movie['revenue']>0 and movie['budget']>20]
    movie_info_tuples = [(movie['title'], movie['budget'], movie['revenue'], movie['imdb_rating'], movie['director'], movie['runtime']) for movie in movies_with_budget_and_rev]
    return movie_info_tuples

def revenue_budget_scatter_graph():
    movie_info = movie_info_tuples()
    return dcc.Graph(
        id='budget-vs-revenue',
        figure={
            'data': [
                go.Scatter(
                    x=[info[1] for info in movie_info],
                    y=[info[2] for info in movie_info],
                    text=[info[0] for info in movie_info],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'}
    },)],
            'layout': go.Layout(
                title='Budget vs Revenue',
                xaxis={'type': 'log', 'title': 'Budget'},
                yaxis={'type': 'log', 'title': 'Revenue'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
    )})

def budget_imdb_scatter_graph():
    movie_info = movie_info_tuples()
    return dcc.Graph(
        id='budget-vs-imdb_rating',
        figure={
            'data': [
                go.Scatter(
                    x=[info[1] for info in movie_info],
                    y=[info[3] for info in movie_info],
                    text=[info[0] for info in movie_info],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'}
    },)],
            'layout': go.Layout(
                title='Budget vs IMDb Rating',
                xaxis={'type': 'log', 'title': 'Budget'},
                yaxis={'type': 'log', 'title': 'IMDb Rating'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
    )})

def revenue_imdb_scatter_graph():
    movie_info = movie_info_tuples()
    return dcc.Graph(
        id='revenue-vs-imdb_rating',
        figure={
            'data': [
                go.Scatter(
                    x=[info[2] for info in movie_info],
                    y=[info[3] for info in movie_info],
                    text=[info[0] for info in movie_info],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'}
    },)],
            'layout': go.Layout(
                title='Revenue vs IMDb Rating',
                xaxis={'type': 'log', 'title': 'Revenue'},
                yaxis={'type': 'log', 'title': 'IMDb Rating'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
    )})

def generate_table(data):
    return html.Table(id='movie-table', children=
        [html.Tr(id='headers', children=[
            html.Th(col) for col in data[0].keys()])]
        +
        [html.Tr(id='row-data', children=[
            html.Td(data_dict[column]) for column
            in data_dict.keys()
        ]) for data_dict in data]
    )

def show_movies_in_month(month):
    movies_in_month = movies_by_month(month)
    return generate_table(movies_in_month)

def movie_runtimes():
    movie_info = movie_info_tuples()
    runtimes = [info[5] for info in movie_info]
    movies = [info[0] for info in movie_info]
    profit = [(info[2]-info[1]) for info in movie_info]
    return dcc.Graph(
        id='runtime_vs_profit',
        figure={
            'data': [
                go.Scatter(
                    x=runtimes, y=profit,
                    text=movies, mode='markers',
                    opacity=0.7,
                    line = dict(
                    color = ('rgb(205, 12, 24)'), width = 4,
                    dash = 'dash'),
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'},},
                    )],
            'layout': go.Layout(
                title='Runtime vs Profit',
                xaxis={'type': 'log', 'title': 'Runtime'},
                yaxis={'type': 'log', 'title': 'Profit'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
    )})

def imdb_vs_profit():
    movie_info = movie_info_tuples()
    movies = [info[0] for info in movie_info]
    imdb_rating = [info[3] for info in movie_info]
    profit = [(info[2]-info[1]) for info in movie_info]
    return dcc.Graph(
        id='imdb_vs_profit',
        figure={
            'data': [
                go.Scatter(
                    x=profit, y=imdb_rating,
                    text=movies, mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 10,
                        'line': {'width': 0.5, 'color': 'white'},},
                    )],
            'layout': go.Layout(
                title='IMDb vs Profit',
                xaxis={'type': 'log', 'title': 'Profit'},
                yaxis={'title': 'IMDb Rating'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
    )})
