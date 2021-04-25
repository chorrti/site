import datetime
import sqlalchemy
from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from . db_session import SqlAlchemyBase


class Builds(SqlAlchemyBase):
    __tablename__ = 'build_posts'
    # столбцы таблицы build_posts
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    character = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    character_class = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    artefacts = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    weapon = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    talents = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relation('User')


class BuildForm(FlaskForm):
    character = StringField('Персонаж', validators=[DataRequired()])
    character_class = StringField('Класс персонажа', validators=[DataRequired()])
    artefacts = TextAreaField('Список артефактов', validators=[DataRequired()])
    weapon = TextAreaField('Оружие', validators=[DataRequired()])
    talents = TextAreaField('Cписок необходимых талантов')
    content = TextAreaField("Доп.описание")
    submit = SubmitField('Применить')
