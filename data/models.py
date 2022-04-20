import sqlalchemy
from sqlalchemy import orm, UniqueConstraint

from data.db_session import SqlAlchemyBase


class Statistics(SqlAlchemyBase):
    __tablename__ = 'statistics'
    user = orm.relation('Users')
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    name = sqlalchemy.Column(sqlalchemy.String)
    value = sqlalchemy.Column(sqlalchemy.Integer)


class Users(SqlAlchemyBase):
    __table_args__ = (
        UniqueConstraint('discord_id', 'guild_id'),
    )
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    discord_id = sqlalchemy.Column(sqlalchemy.Integer)
    guild_id = sqlalchemy.Column(sqlalchemy.Integer)


class Money(SqlAlchemyBase):
    __tablename__ = 'money'
    user = orm.relation('Users')
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    balance = sqlalchemy.Column(sqlalchemy.Integer)
