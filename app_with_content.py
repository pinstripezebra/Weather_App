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
from utility.measurement import find_optimal_window


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
acceptable_pages = ['Home1', 'Maps1']

# defining optimal conditions to compare against weather forecast
optimal_conditions = {'temperature_2m': 30,
                      'cloudcover': 0.1,
                      'windspeed_10m': 0.1,
                      'precipitation_probability': 0.1}

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


# definign layout with dcc.store component to ensure all pages have access to weather forecast
app.layout = html.Div([
        dcc.Store(id='stored-forecast', storage_type='local'), # for storing weather forecast in dataframe
        dcc.Store(id='optimal-conditions', storage_type='local'), # for storing ideal conditions for user
        dcc.Store(id='location-storage', storage_type='local'), # for storing users latitude/longitude
        html.Div([sidebar,
        html.Div([
                dash.page_container
        ])
    ])

])


# Callback function to pull weather forecast data and store it for use on pages
@callback(
    [Output('stored-forecast', 'data'),
     Output('optimal-conditions', 'data'),
     Input('location-storage', 'data')],
    [Input('login-button', 'n_clicks')])

def login_button_click(n_clicks):

    # Logging forecast to store for consumption in other pages
    repull_data = True
    df1 = data_pipeline(repull_data, LATITUDE, LONGITUDE)
    df1['time'] = df1.index
    df1.reset_index(drop = True)
    df1['time'] = pd.to_datetime(df1['time'])
    forecasted_conditions = {'temperature_2m': df1['temperature_2m'].to_list(),
                            'cloudcover': df1['cloudcover'].to_list(),
                            'windspeed_10m': df1['windspeed_10m'].to_list(),
                            'precipitation_probability': df1['precipitation_probability'].to_list()}

    # Rating weather conditions and adding overall score to dataframe
    conditions = find_optimal_window(optimal_conditions, forecasted_conditions, LATITUDE, LONGITUDE)
    df1['Forecast_Score'] = conditions['Score'].to_list()
    location = {'latitude': LATITUDE,
                        'longitude': LONGITUDE}
            
    # navigate to landing page if logged in successfully 
    return df1.to_json(date_format='iso', orient='split'), optimal_conditions, location
       


# Running the app
if __name__ == '__main__':
    app.run_server(debug=True)
