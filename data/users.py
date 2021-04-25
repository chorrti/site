import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    # информация о пользователях
    __tablename__ = 'users'
    # столбцы таблицы users:
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, unique=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    #pic = sqlalchemy.Column(sqlalchemy.String, nullable=False, default='default.jpg')
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    # сообщения пользователя
    news = orm.relation('News', back_populates='user')
    build_posts = orm.relation('Builds', back_populates='user')
    team_posts = orm.relation('Teams', back_populates='user')

    def set_password(self, password):
        # создание хэша пароля
        # (используется при регистрации пользователя)
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        # проверка пароля
        return check_password_hash(self.hashed_password, password)
