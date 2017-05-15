import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine("mysql://root:rntekrrntekr1!@45.77.19.179:4306/farms?use_unicode=True&charset=utf8", encoding='utf-8', pool_size=100, max_overflow=200)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()