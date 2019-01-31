import sqlalchemy

from app.config import Config
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ModelBase = declarative_base()

class Connection:
    def __init__(self):
        connection_string = f"mysql://{Config.d['database']['user']}:{Config.d['database']['password']}@{Config.d['database']['address']}:{Config.d['database']['port']}/{Config.d['database']['db']}"
        engine = sqlalchemy.create_engine(f"{connection_string}?use_unicode=True&charset=utf8", encoding='utf-8', pool_size=2, max_overflow=200)
        Connection.session = scoped_session(sessionmaker(bind=engine))
        ModelBase.query = Connection.session.query_property()