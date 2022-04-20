class GuildData:
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id

        self.guild = None
        self.members = None

    def get_guild(self):
        if self.guild is None:
            self.guild = self.bot.get_guild(self.guild_id)
        return self.guild

    def get_members(self):
        if self.members is None:
            self.members = list(filter(lambda x: not x.bot, self.get_guild().members))

        return self.members


