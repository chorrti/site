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
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # сообщения пользователя
    news = orm.relation('News', back_populates='user')

    def set_password(self, password):
        # создание хэша пароля
        # (используется при регистрации пользователя)
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        # проверка пароля
        return check_password_hash(self.hashed_password, password)
