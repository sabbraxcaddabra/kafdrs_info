from dash import dcc
from dash import html
from dash import Input, Output, State, callback

import models
from flask_login import login_user, logout_user, LoginManager
from werkzeug.security import check_password_hash

login_manager = LoginManager()
login_manager.login_view = '/login'

login =  html.Div([
    dcc.Location(id='url_login', refresh=True),
    html.H2('''Авторизуйтесь, чтобы продолжить''', id='h1'),
    dcc.Input(placeholder='Введите имя пользователя', type='text', id='uname-box'),
    dcc.Input(placeholder='Введите пароль', type='password', id='pwd-box'),
    html.Button(children='Войти', n_clicks=0, type='submit', id='login-button') ,
    html.Div(children='', id='output-state')
])

@login_manager.user_loader
def load_user(user_id):
    return models.Users.query.get(int(user_id))

@callback(
    Output('url_login', 'pathname'),
    [Input('login-button', 'n_clicks')],
    [State('uname-box', 'value'), State('pwd-box', 'value')])
def successful(n_clicks, input1, input2):
    user = models.Users.query.filter_by(username=input1).first()
    if user:
        if check_password_hash(user.password, input2):
            login_user(user)
            return f'/{input1}'
        else:
            pass
    else:
        pass