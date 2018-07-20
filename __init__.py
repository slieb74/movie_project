import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_sqlalchemy import SQLAlchemy

app = dash.Dash(__name__, url_base_pathname='/dashboard')

app.server.config['DEBUG'] = True
app.server.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app.server)
