import os
import dash
from dash.dependencies import Input, Output, State
from dash import html, dcc

from typing import Tuple

import auth_page, stats_page

from flask_login import current_user, logout_user
import configparser

KAF_LIST = ["a8", "e3"]

# def get_usrname_pwd() -> Tuple[str, str]:
#     # Функция возвращает имя пользователя и пароль (в виде кортежа из двух строк) для текущей сессии
#     # Нужно для того чтобы понимать с какой кафедры пользователь
#     header = flask.request.headers.get('Authorization', None)
#     username_password = base64.b64decode(header.split('Basic ')[1])
#     username_password_utf8 = username_password.decode('utf8')
#     username, password = username_password_utf8.split(':', 1)
#     return username, password

# def get_valid_usrname_pwd_list() -> dict:
#     # Функция возвращает словарь с доступными логинами-паролями
#     with open('config.json', encoding='utf-8') as config_fp:
#         valid_usrname_pwd_list = json.load(config_fp)["authorization"]
#     return valid_usrname_pwd_list


# VALID_USERNAME_PASSWORD_PAIRS = get_valid_usrname_pwd_list()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
        return auth_page.login
    elif pathname[1:] in KAF_LIST:
        if current_user.is_authenticated:
            return stats_page.generate_layout(pathname[1:].upper())
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)

