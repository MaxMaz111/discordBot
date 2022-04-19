from data import db_session


class DbData:
    def __init__(self, db_name: str):
        db_session.global_init(db_name)
