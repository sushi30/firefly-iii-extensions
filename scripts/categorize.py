from sqlalchemy import create_engine


def by_name(storage):
    engine = create_engine(storage)
