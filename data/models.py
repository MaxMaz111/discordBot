import sqlalchemy
from sqlalchemy import orm, UniqueConstraint

from data.db_session import SqlAlchemyBase


class Statistics(SqlAlchemyBase):
    __tablename__ = 'statistics'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)


class UserStatistics(SqlAlchemyBase):
    __table_args__ = (
        UniqueConstraint('user_id', 'statistic_id'),
    )
    __tablename__ = 'user_statistics'
    statistics = orm.relation('Statistics')
    user = orm.relation('Users')
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    statistic_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('statistics.id'))
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
