import base64
from re import I
import dash
from dash.dependencies import Input, Output
from dash_auth import BasicAuth
from dash import html, dcc
import dash_auth
import flask
import json
from typing import Tuple

def get_usrname_pwd() -> Tuple[str, str]:
    # Функция возвращает имя пользователя и пароль (в виде кортежа из двух строк) для текущей сессии
    # Нужно для того чтобы понимать с какой кафедры пользователь
    header = flask.request.headers.get('Authorization', None)
    username_password = base64.b64decode(header.split('Basic ')[1])
    username_password_utf8 = username_password.decode('utf8')
    username, password = username_password_utf8.split(':', 1)
    return username, password

def get_valid_usrname_pwd_list() -> dict:
    # Функция возвращает словарь с доступными логинами-паролями
    with open('config.json', encoding='utf-8') as config_fp:
        valid_usrname_pwd_list = json.load(config_fp)["authorization"]
    return valid_usrname_pwd_list


VALID_USERNAME_PASSWORD_PAIRS = get_valid_usrname_pwd_list()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.layout = html.Div([
    html.H1('Welcome to the app'),
    html.H3('You are successfully authorized'),
    dcc.Dropdown(['A', 'B'], 'A', id='dropdown'),
    dcc.Graph(id='graph')
], className='container')

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_graph(dropdown_value):
    print(get_usrname_pwd())
    return {
        'layout': {
            'title': 'Graph of {}'.format(dropdown_value),
            'margin': {
                'l': 20,
                'b': 20,
                'r': 10,
                't': 60
            }
        },
        'data': [{'x': [1, 2, 3], 'y': [4, 1, 2]}]
    }

if __name__ == '__main__':
    app.run_server(debug=True)

