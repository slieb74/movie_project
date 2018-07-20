from flask import render_template, jsonify, json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_sqlalchemy import SQLAlchemy
from __init__ import app
from models import Movie, Director, Genre, MovieGenre

app.layout = html.Div(children=[
    html.H1('Welcome to our Movie Database.'),
    html.H3('To fully enjoy your experience, play around with different routes to learn more about movie performance.')])
