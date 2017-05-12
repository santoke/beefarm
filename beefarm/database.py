import sqlalchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = sqlalchemy.create_engine("mysql://root:rntekrrntekr1!@45.77.19.179:4306/farms")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()