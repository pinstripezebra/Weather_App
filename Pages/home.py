import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table, ctx

dash.register_page(__name__, path='/landing')

# Defining layout
layout = html.Div([
    html.H1('Our Home Page for Weather Forecasting')
])
