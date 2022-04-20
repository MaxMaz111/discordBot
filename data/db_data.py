from data import db_session
from data.models import Users, Money


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

    def set_zero(self, user: Users) -> Money:
        money = Money()
        money.user_id = user.id
        money.balance = 0
        self.db_sess.add(money)
        self.db_sess.commit()
        return money

    def set_money(self, user: Users, amount: int) -> Money:
        money = self.get_money(user)
        money.balance = amount
        self.db_sess.commit()
        return money

    def add_money(self, user: Users, amount: int) -> Money:
        money = self.get_money(user)
        money.balance += amount
        self.db_sess.commit()
        return money

    def get_money(self, user: Users) -> Money:
        user_money = self.db_sess.query(Money).filter(Money.user_id == user.id).first()
        if not user_money:
            user_money = self.set_zero(user)
        return user_money
