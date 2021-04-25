import datetime
import sqlalchemy
from flask_wtf import FlaskForm
from sqlalchemy import orm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from . db_session import SqlAlchemyBase


class Teams(SqlAlchemyBase):
    __tablename__ = 'team_posts'
    # столбцы таблицы build_posts
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    character_1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    character_2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    character_3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    character_4 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    character_class_1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    character_class_2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    character_class_3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    character_class_4 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    artefacts = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    talents = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    user = orm.relation('User')


class TeamForm(FlaskForm):
    character_1 = StringField('Персонаж_1', validators=[DataRequired()])
    character_2 = StringField('Персонаж_2', validators=[DataRequired()])
    character_3 = StringField('Персонаж_3', validators=[DataRequired()])
    character_4 = StringField('Персонаж_4', validators=[DataRequired()])
    character_class_1 = StringField('Класс персонажа_1', validators=[DataRequired()])
    character_class_2 = StringField('Класс персонажа_2', validators=[DataRequired()])
    character_class_3 = StringField('Класс персонажа_3', validators=[DataRequired()])
    character_class_4 = StringField('Класс персонажа_4', validators=[DataRequired()])
    artefacts = TextAreaField('Список артефактов', validators=[DataRequired()])
    talents = TextAreaField('Cписок необходимых талантов')
    content = TextAreaField("Доп.описание")
    submit = SubmitField('Применить')
