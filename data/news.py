import datetime
import sqlalchemy
from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from . db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'
    # столбцы таблицы news
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relation('User')


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание")
    submit = SubmitField('Применить')
