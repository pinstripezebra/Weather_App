import dash
from dash import html, Dash, dcc, callback,Input, Output,dash_table, ctx

dash.register_page(__name__, path='/maps')

# Defining layout
layout = html.Div([
    html.H1('Our Maps page')
])
