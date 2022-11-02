import json
import sqlite3
from sqlalchemy import Table, create_engine
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin

conn = sqlite3.connect('./instance/data.sqlite')

engine = create_engine('sqlite:///instance/data.sqlite')

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable = False)
    # email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String)

Users_tbl = Table('users', Users.metadata)

if __name__ == '__main__':
    from werkzeug.security import generate_password_hash
    def create_users_table():
        Users.metadata.create_all(engine)

    with open('passwords.json', encoding='utf8') as pwd_fp:
        pwd_dict = json.load(pwd_fp)

    #create the table
    # create_users_table()
    conn = engine.connect()
    for username, pwd in pwd_dict.items():

        ins = Users_tbl.insert().values(username=username, password=generate_password_hash(pwd))
        conn.execute(ins)

    conn.close()