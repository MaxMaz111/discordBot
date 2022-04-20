from data import db_session
from data.models import Users


class DbData:
    def __init__(self, db_name: str):
        db_session.global_init(db_name)
        self.db_sess = db_session.create_session()

    def get_user(self, discord_id: int, guild_id: int):
        user = self.db_sess.query(Users).filter(Users.guild_id == guild_id, Users.discord_id == discord_id).first()
        if not user:
            user = self.add_user(discord_id, guild_id)
        return user

    def add_user(self, discord_id: int, guild_id: int):
        user = Users()
        user.discord_id = discord_id
        user.guild_id = guild_id
        self.db_sess.add(user)
        self.db_sess.commit()
        return user
