import typing
from typing import List, Tuple

from data import db_session
from data.models import Users, Money, Statistics, UserStatistics, StatisticType


class DbData:
    def __init__(self, db_name: str):
        db_session.global_init(db_name)
        self.db_sess = db_session.create_session()

    def get_user(self, discord_id: int, guild_id: int) -> Users:
        user = self.db_sess.query(Users).filter(Users.guild_id == guild_id, Users.discord_id == discord_id).first()
        if not user:
            user = self.add_user(discord_id, guild_id)
        return user

    def add_user(self, discord_id: int, guild_id: int) -> Users:
        user = Users()
        user.discord_id = discord_id
        user.guild_id = guild_id
        self.db_sess.add(user)
        self.db_sess.commit()
        return user

    def init_money(self, user: Users) -> Money:
        money = Money()
        money.user_id = user.id
        money.balance = 0
        self.db_sess.add(money)
        self.db_sess.commit()
        return money

    def set_money(self, amount: int, user: Users = None, money: Money = None) -> Money:
        if money is None:
            money = self.get_money(user)
        money.balance = amount
        self.db_sess.commit()
        return money

    def update_money(self, user: Users, delta: int) -> Money:
        money = self.get_money(user)
        return self.set_money(money=money, amount=money.balance + delta)

    def get_money(self, user: Users) -> Money:
        user_money = self.db_sess.query(Money).filter(Money.user_id == user.id).first()
        if not user_money:
            user_money = self.init_money(user)
        return user_money

    def top_users_by_money(self, guild_id: int, member_ids: typing.Set[int], limit: int) -> List[Tuple[int, int]]:
        return self.db_sess.query(Users.discord_id, Money.balance) \
            .filter(Users.guild_id == guild_id and Users.discord_id in member_ids) \
            .join(Money) \
            .order_by(Money.balance.desc()) \
            .limit(limit) \
            .all()

    def send_money(self,
                   sender: Users,
                   recipient: Users,
                   amount: int,
                   sender_money: Money = None,
                   recipient_money: Money = None):
        if sender_money is None:
            sender_money = self.get_money(sender)

        if recipient_money is None:
            recipient_money = self.get_money(recipient)

        sender_money.balance -= amount
        recipient_money.balance += amount

        self.db_sess.commit()

    def add_statistic(self, statistic_type: StatisticType) -> Statistics:
        statistic = Statistics()
        statistic.name = statistic_type.value

        self.db_sess.add(statistic)
        self.db_sess.commit()

        return statistic

    def get_statistic(self, statistic_type: StatisticType) -> Statistics:
        statistic = self.db_sess.query(Statistics).filter(Statistics.name == statistic_type.value).first()
        if not statistic:
            statistic = self.add_statistic(statistic_type)
        return statistic

    def init_user_statistic(self,
                            user: Users,
                            statistic: Statistics) -> UserStatistics:
        user_statistic = UserStatistics()
        user_statistic.user_id = user.id
        user_statistic.statistic_id = statistic.id
        user_statistic.value = 0

        self.db_sess.add(user_statistic)
        self.db_sess.commit()

        return user_statistic

    def get_user_statistic(self,
                           user: Users,
                           statistic: Statistics = None,
                           statistic_type: StatisticType = None) -> UserStatistics:
        if not statistic:
            statistic = self.get_statistic(statistic_type)

        user_statistic = self.db_sess.query(UserStatistics) \
            .filter(UserStatistics.user_id == user.id and UserStatistics.statistic_id == statistic.id) \
            .first()

        if not user_statistic:
            user_statistic = self.init_user_statistic(user, statistic)

        return user_statistic

    def update_user_statistic(self,
                              user: Users,
                              statistic_type: StatisticType,
                              new_value: int = None,
                              delta: int = None):
        user_statistic = self.get_user_statistic(user=user, statistic_type=statistic_type)

        old_value = user_statistic.value
        if new_value is None:
            new_value = old_value + delta

        user_statistic.value = new_value

        self.db_sess.commit()
