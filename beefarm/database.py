import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

connection_string = f"mysql://{config.d['database']['user']}:{config.d['database']['password']}@{config.d['database']['address']}:{config.d['database']['port']}/{config.d['database']['db']}"
engine = sqlalchemy.create_engine(f"{connection_string}?use_unicode=True&charset=utf8", encoding='utf-8', pool_size=2, max_overflow=200)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()