from dash import Dash, html


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets', assets_url_path='/assets/')

app.layout = [html.Div(children='This is the home page of our weather app')]

if __name__ == '__main__':
    app.run(debug=True)