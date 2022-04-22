def get_mentioned_id(ctx, mentioned_id_argument):
    mentioned_id = ctx.message.mentions[0].id if ctx.message.mentions else mentioned_id_argument
    return int(mentioned_id)


def get_author(ctx):
    return ctx.message.author


def to_nickname(member) -> str:
    return member.name + '#' + member.discriminator
