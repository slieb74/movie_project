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

def movies_by_month(month):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_month = [movie for movie in all_movies_dict if int(movie['release_date'][5:7]) == month]
    return movies_in_month

def movie_count_by_month_graph():
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
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
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    avg_revenue = [avg_revenue_by_month(month) for month in months]
    return dcc.Graph(
            id='bar-graph-avg-rev-months',
            figure={'data': [
                    {'x': [calendar.month_name[month] for month in months], 'y': avg_revenue, 'type': 'bar'}],
                'layout': {
                    'title': 'Average Revenue by Release Month'
    }})

def avg_revenue_by_season(season):
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_in_season = [movie for movie in all_movies_dict if movie['release_date'][5:7] in season_dict.get(season)]
    movies_excl_zero_revenue = [movie for movie in movies_in_season if movie['revenue'] > 0]
    sum_revenue = sum([movie['revenue']for movie in movies_excl_zero_revenue])
    avg_revenue = round(sum_revenue/len(movies_excl_zero_revenue))
    return '${:,}'.format(avg_revenue)

def avg_revenue_season_graph():
    months = [1,2,3,4,5,6,7,8,9,10,11,12]
    seasons=['summer', 'fall', 'winter', 'spring']
    avg_revenue = [avg_revenue_by_season(season) for season in seasons]
    return dcc.Graph(
            id='bar-graph-avg-rev-seasons',
            figure= {'data': [
                    {'x': seasons, 'y': avg_revenue, 'type': 'bar'}],
                'layout': {
                    'title': 'Average Revenue by Season Released'
    }})
    # return dcc.Graph(
    #         id='pie-graph-avg-rev-seasons',
    #         figure= {
    #             'data': [
    #                go.Pie(
    #                     labels=seasons, values=avg_revenue)
    #                     ,],
    #             'layout': go.Layout(
    #                 title='Average Revenue by Season Released')
    #                 })

def revenue_budget_by_movie():
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_with_budget_and_rev = [movie for movie in all_movies_dict if movie['revenue']>0 and movie['budget']>20]
    budget_revenue_tuples = [(movie['title'], movie['budget'], movie['revenue']) for movie in movies_with_budget_and_rev]
    return budget_revenue_tuples

def revenue_budget_scatter_graph():
    budget_revenue_tuples = revenue_budget_by_movie()
    return dcc.Graph(
        id='budget-vs-revenue',
        figure={
            'data': [
                go.Scatter(
                    x=[budget_revenue_tuple[1] for budget_revenue_tuple in budget_revenue_tuples],
                    y=[budget_revenue_tuple[2] for budget_revenue_tuple in budget_revenue_tuples],
                    text=[budget_revenue_tuple[0] for budget_revenue_tuple in budget_revenue_tuples],
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

def budget_imdb_rating_by_movie():
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_with_budget_not_null = [movie for movie in all_movies_dict if movie['budget']>20]
    budget_imdb_tuples = [(movie['title'], movie['budget'], movie['imdb_rating']) for movie in movies_with_budget_not_null]
    return budget_imdb_tuples

def budget_imdb_scatter_graph():
    budget_imdb_tuples = budget_imdb_rating_by_movie()
    return dcc.Graph(
        id='budget-vs-imdb_rating',
        figure={
            'data': [
                go.Scatter(
                    x=[budget_imdb_tuple[1] for budget_imdb_tuple in budget_imdb_tuples],
                    y=[budget_imdb_tuple[2] for budget_imdb_tuple in budget_imdb_tuples],
                    text=[budget_imdb_tuple[0] for budget_imdb_tuple in budget_imdb_tuples],
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
    budget_imdb_tuples = budget_imdb_rating_by_movie()
    budget_revenue_tuples = revenue_budget_by_movie()
    return dcc.Graph(
        id='revenue-vs-imdb_rating',
        figure={
            'data': [
                go.Scatter(
                    x=[budget_revenue_tuple[2] for budget_revenue_tuple in budget_revenue_tuples],
                    y=[budget_imdb_tuple[2] for budget_imdb_tuple in budget_imdb_tuples],
                    text=[budget_imdb_tuple[0] for budget_imdb_tuple in budget_imdb_tuples],
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


app.layout = html.Div(children=[
    dcc.Dropdown(
        id='class-dropdown',
        options=[
            {'label': 'Movies', 'value': 'M'},
            {'label': 'Genres', 'value': 'G'},
            {'label': 'Directors', 'value': 'D'},
        ],
        value='M'
    ),
    html.Div(id='class-choices'),

    dcc.Dropdown(
            id='movie-dropdown',
            options=[
                {'label': 'Count', 'value': 'CT'},
                {'label': 'Average Revenue per Month', 'value': 'AVG-Month'},
                {'label': 'Average Revenue per Season', 'value': 'AVG-Season'},
                {'label': 'Budget/Revenue', 'value': 'Bud/Rev'},
                {'label': 'Budget/IMDb Rating', 'value': 'Bud/IMDb'},
                {'label': 'Revenue/IMDb Rating', 'value': 'Rev/IMDb'}
            ],
            value="CT"),
    html.Div(id='movie-graphs')
])

@app.callback(
    Output(component_id = 'movie-graphs', component_property='children'),
    [Input(component_id= 'movie-dropdown', component_property='value')]
    )

def update_output(value):
    if value=='CT':
        return movie_count_by_month_graph()
    elif value=='AVG-Month':
        return avg_revenue_month_graph()
    elif value=='AVG-Season':
        return avg_revenue_season_graph()
    elif value=='Bud/Rev':
        return revenue_budget_scatter_graph()
    elif value=='Bud/IMDb':
        return budget_imdb_scatter_graph()
    elif value=='Rev/IMDb':
        return revenue_imdb_scatter_graph()

# @app.callback(
#     Output(component_id = 'class-choices', component_property='children'),
#     [Input(component_id= 'class-dropdown', component_property='value')]
#     )
