import os
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc

from typing import Tuple

import auth_page, stats_page

from flask_login import current_user, logout_user
import configparser
import dash_bootstrap_components as dbc

KAF_LIST = stats_page.SPEC_CODES_DICT.keys()

external_stylesheets = [dbc.themes.GRID,
                        dbc.themes.BOOTSTRAP,
                        'https://codepen.io/chriddyp/pen/bWLwgP.css'
                        ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True,
                meta_tags=[
                    {'name': 'viewport', 'content': 'width=device-width, initial-scale=0.7'}
                ]
                )

server = app.server

app.config.suppress_callback_exceptions = True

config = configparser.ConfigParser()

server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///data.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

auth_page.models.db.init_app(server)

auth_page.login_manager.init_app(server)

app.layout = html.Div([
    html.Div(id='page-content', className='content'), dcc.Location(id='url', refresh=False)
], className='container')

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname in ('/', '/logout'):
        logout_user()
        return auth_page.login
    elif pathname[1:] in KAF_LIST:
        if current_user.is_authenticated:
            return stats_page.generate_layout(pathname[1:].upper())
    else:
        return '404'


if __name__ == '__main__':
    app.run(debug=True)

