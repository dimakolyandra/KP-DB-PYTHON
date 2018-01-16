from db_connection.connection import Base
from sqlalchemy import Column, String


class Currency(Base):
    __tablename__ = 'CURRENCY'

    iso = Column(String(3), primary_key=True)
    state = Column(String(100))
    currency_name = Column(String(100))
    issuing_center = Column(String(100))
    variable_currency = Column(String(100))
