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

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
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
    movie_info_tuples = [(movie['title'], movie['budget'], movie['revenue'], movie['imdb_rating'], movie['director']) for movie in movies_with_budget_and_rev]
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
