# For data manipulation, visualization, app
import dash
from dash import Dash, dcc, html, callback, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os 
from dotenv import find_dotenv, load_dotenv
import json
from utility.data_query import data_pipeline
import flask



# loading environmental variables
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
LATITUDE, LONGITUDE = float(os.getenv("LATITUDE")), float(os.getenv("LONGITUDE"))
repull_data = True


# defining path
path = os.path.dirname(__file__)

# loading Data
df1 = data_pipeline(repull_data, LATITUDE, LONGITUDE)

# Loading json files containing component styles
SIDEBAR_STYLE , CONTENT_STYLE = {}, {}
with open(path + '/style/sidebar_style.json') as f:
    SIDEBAR_STYLE = json.load(f)
with open(path + '/style/content_style.json') as f:
    CONTENT_STYLE = json.load(f)


# defining and Initializing the app
server = flask.Flask(__name__)
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets', assets_url_path='/assets/', server = server)
acceptable_pages = ['Home', 'Maps']

# Defining components
sidebar = html.Div(children = [
            html.Img(
                        alt="Link to Github",
                        src="./assets/app_logo.png",
                        style={'height':'10%', 'width':'40%', 'margin': 'auto'}
                    ),
            html.H3("Pages"),
            html.Hr(),
            html.Div([ 
                dbc.Nav([
                    dbc.NavLink(f"{page['name']}", href = page["relative_path"]) for page in dash.page_registry.values() if page["name"]  in acceptable_pages
                ], vertical=True)

            ]),
            html.H3("Description"),
            html.P(
                "This app brings you hourly weather forecasts from OpenMeteo to help plan your day.", className="text"
            ),
            html.H3("Code"
            ),
            html.P(
                "The complete code for this project is available on github.", className="text"
            ),
            html.A(
                href="https://github.com/pinstripezebra/Dash-Tutorial",
                children=[
                    html.Img(
                        alt="Link to Github",
                        src="./assets/github_logo.png",
                        style={'height':'3%', 'width':'8%'}
                    )
                ],
                style = {'color':'black'}
            )

        ], style=SIDEBAR_STYLE
    )


app.layout = html.Div([sidebar,
    html.Div([
            dash.page_container
    ], style=CONTENT_STYLE)
])



# Running the app
if __name__ == '__main__':
    app.run_server(debug=True)
