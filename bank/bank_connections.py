from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

Base = declarative_base()


def get_session(conn_string):
    engine = create_engine(conn_string, poolclass=StaticPool)
    Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    return Session()

sber_conn = get_session(
    'oracle+cx_oracle://sberbank_sys:1234@localhost:1521/ORCL')

forex_conn = get_session(
    'oracle+cx_oracle://forex_sys:1234@localhost:1521/ORCL')

alpha_conn = get_session(
    'oracle+cx_oracle://alpha_bank_sys:1234@localhost:1521/ORCL')

connection_dict = {
    '3': sber_conn,
    '4': forex_conn,
    '5': alpha_conn
}
