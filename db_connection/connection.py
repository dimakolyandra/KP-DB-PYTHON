from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


conn_string = 'oracle+cx_oracle://dima:1234@localhost:1521/ORCL'

Base = declarative_base()


def get_session():
    engine = create_engine(conn_string, poolclass=StaticPool)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return Session()
