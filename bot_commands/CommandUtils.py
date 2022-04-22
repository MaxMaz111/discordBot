def get_mentioned_id(ctx, recipient_id_argument):
    recipient_id = ctx.message.mentions[0].id if ctx.message.mentions else recipient_id_argument
    return int(recipient_id)


def get_author(ctx):
    return ctx.message.author


def to_nickname(member) -> str:
    return member.name + '#' + member.discriminator
