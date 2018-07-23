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
from genre_routes import *
from director_routes import *

##################### DASH LAYOUT ##########################

app.layout = html.Div(children=[
    html.H1('Welcome to our Movie Database.'),
    html.H3('To fully enjoy your experience, play around with different routes to learn more about movie performance.'),

    dcc.Tabs(
        tabs=[
            {'label': 'Movies', 'value': 'M'},
            {'label': 'Genres', 'value': 'G'},
            {'label': 'Directors', 'value': 'D'},
        ],
        value='M',
        id='tabs'
    ),
    html.Div(id='tab-output'),
    # option 1
    # container html.Div(children=movies_view)
    # movies_view = html.Div(id='movies_view', children=
    #     dcc.Graph
    # )
    # option 2
    # movies_view = html.Div(id='movies_view', children=
    #     dcc.Graph
    # )

    dcc.Dropdown(
            id='class-dropdown',
            options=[],
            value='M-CT'
    ),
    html.Div(id='class-graphs'),

    html.Label(),
    dcc.RadioItems(
        id='radio-items',
        options=[],
        value=0,
        labelStyle={'display': 'inline-block'}
    ),
    html.Div(id='month-graphs'),
    dcc.Checklist(
        id='genre-specific',
        options=[],
        values = [1],
        labelStyle={'display': 'inline-block'}
    ),
    html.Div(id='month_genres')
])

@app.callback(
    Output(component_id = 'class-dropdown', component_property='options'),
    [Input(component_id= 'tabs', component_property='value')]
    )
def update_dropdown(value):
    if value=='M':
        return [{'label': 'Count', 'value': 'M-CT'},
        {'label': 'Average Revenue per Month', 'value': 'AVG-Month'},
        {'label': 'Average Revenue per Season', 'value': 'AVG-Season'},
        {'label': 'Budget/Revenue', 'value': 'Bud/Rev'},
        {'label': 'Budget/IMDb Rating', 'value': 'Bud/IMDb'},
        {'label': 'Revenue/IMDb Rating', 'value': 'Rev/IMDb'},
        {'label': 'Runtime/Profit', 'value':'RT/Profit'},
        {'label': 'IMDb Rating/Profit', 'value':'IMDb/Profit'}
        ]
    elif value=='G':
        return [{'label': 'Count', 'value': 'G-CT'},
        {'label': 'Total', 'value': 'TOT'},
        {'label': 'Average', 'value': 'AVG'}
        ]
    elif value=='D':
        return [{'label': 'Count', 'value': 'D-CT'},
        {'label': 'Revenue', 'value': 'D-Rev'}
        ]

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
    elif value == 'RT/Profit':
        return movie_runtimes()
    elif value == 'IMDb/Profit':
        return imdb_vs_profit()
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
    elif value == 'D-CT':
        return director_count()
    elif value =='D-Rev':
        return director_revenue_graph()

#create radio items for movie and genre dropdowns
@app.callback(
    Output(component_id = 'radio-items', component_property='options'),
    [Input(component_id= 'tabs', component_property='value')
    ])
def update_radio_items(value):
    if value=='M':
        return [{'label': 'January', 'value': 1},
        {'label': 'February', 'value': 2},
        {'label': 'March', 'value': 3},
        {'label': 'April', 'value': 4},
        {'label': 'May', 'value': 5},
        {'label': 'June', 'value': 6},
        {'label': 'July', 'value': 7},
        {'label': 'August', 'value': 8},
        {'label': 'September', 'value': 9},
        {'label': 'October', 'value': 10},
        {'label': 'November', 'value': 11},
        {'label': 'December', 'value': 12}]
    elif value=='G':
        return [
        {'label': 'How Many a month', 'value': 'MANY'},
        {'label': 'Revenue', 'value': 'REV'},
        {'label': 'Profit', 'value': 'PRO'}]
    elif value=='D':
        return []

#generate checklists for genre dropdown
@app.callback(
    Output(component_id = 'genre-specific', component_property='options'),
    [Input(component_id= 'tabs', component_property='value')
    ])
def update_checklists(value):
    if value=='G':
        return genre_setup()
    else:
        return []

#revenue secondary graphs for months
@app.callback(
    Output(component_id = 'month-graphs', component_property='children'),
    [Input(component_id= 'tabs', component_property='value'),
    Input(component_id = 'radio-items', component_property='value')],
    )
def update_secondary_graph(value,radio):
    if value=='M':
        return show_movies_in_month(radio)
    else:
        return []

#genre secondary graphs
@app.callback(
    Output('month_genres', 'children'),
    [Input(component_id= 'tabs', component_property='value'),
    Input('genre-specific', 'values'),
    Input ('radio-items', 'value')])
def update_gen_months(genre ,value, radio):
    if genre=='G':
        if radio == 'MANY':
            return genre_months(value)
        elif radio == 'REV':
            return genre_tot_months(value)
        elif radio == 'PRO':
            return genre_profits_months(value)
    else:
        return []
