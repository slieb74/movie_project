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

######################  MOVIES  ######################
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

def movie_info_tuples():
    all_movies_dict = [movie.to_dict() for movie in Movie.query.all()]
    movies_with_budget_and_rev = [movie for movie in all_movies_dict if movie['revenue']>0 and movie['budget']>20]
    movie_info_tuples = [(movie['title'], movie['budget'], movie['revenue'], movie['imdb_rating']) for movie in movies_with_budget_and_rev]
    return movie_info_tuples

def revenue_budget_scatter_graph():
    movie_info_tuples = movie_info_tuples()
    return dcc.Graph(
        id='budget-vs-revenue',
        figure={
            'data': [
                go.Scatter(
                    x=[info[1] for info in movie_info_tuples],
                    y=[info[2] for info in movie_info_tuples],
                    text=[info[0] for info in movie_info_tuples],
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
    movie_info_tuples = movie_info_tuples()
    return dcc.Graph(
        id='budget-vs-imdb_rating',
        figure={
            'data': [
                go.Scatter(
                    x=[info[1] for info in movie_info_tuples],
                    y=[info[3] for info in movie_info_tuples],
                    text=[info[0] for info in movie_info_tuples],
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
    movie_info_tuples = movie_info_tuples()
    return dcc.Graph(
        id='revenue-vs-imdb_rating',
        figure={
            'data': [
                go.Scatter(
                    x=[info[2] for info in movie_info_tuples],
                    y=[info[3] for info in movie_info_tuples],
                    text=[info[0] for info in movie_info_tuples],
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

        # avg_revenue = round(sum_revenue/len(movies_excl_zero_revenue))

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
#Genre avg made
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

##################### DASH LAYOUT ##########################

app.layout = html.Div(children=[
    dcc.Dropdown(
        id='all-dropdown',
        options=[
            {'label': 'Movies', 'value': 'M'},
            {'label': 'Genres', 'value': 'G'},
            {'label': 'Directors', 'value': 'D'},
        ],
        value='M'
    ),
    html.Div(id='all-choices'),

    dcc.Dropdown(
            id='class-dropdown',
            options=[],
            value='M-CT'
    ),
    html.Div(id='class-graphs')
])


@app.callback(
    Output(component_id = 'class-dropdown', component_property='options'),
    [Input(component_id= 'all-dropdown', component_property='value')]
    )
def update_dropdown(value):
    if value=='M':
        return [{'label': 'Count', 'value': 'M-CT'},
        {'label': 'Average Revenue per Month', 'value': 'AVG-Month'},
        {'label': 'Average Revenue per Season', 'value': 'AVG-Season'},
        {'label': 'Budget/Revenue', 'value': 'Bud/Rev'},
        {'label': 'Budget/IMDb Rating', 'value': 'Bud/IMDb'},
        {'label': 'Revenue/IMDb Rating', 'value': 'Rev/IMDb'}
        ]
    elif value=='G':
        return [{'label': 'Count', 'value': 'G-CT'},
        {'label': 'Total', 'value': 'TOT'},
        {'label': 'Average', 'value': 'AVG'}
        ]
    elif value=='D':
        pass

@app.callback(
    Output(component_id = 'class-graphs', component_property='children'),
    [Input(component_id= 'class-dropdown', component_property='value')]
    )
def update_output(value):
    if value=='M-CT':
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
    elif value == 'G-CT':
        return dcc.Graph(
            id = "Genres_total",
            figure = genre_count_layout())
    elif value == 'TOT':
        return dcc.Graph(
            id = "Genres_total",
            figure = genre_total_layout())
    elif value == 'AVG':
        return dcc.Graph(
            id = "Genres_total",
            figure = genre_avg_layout())
