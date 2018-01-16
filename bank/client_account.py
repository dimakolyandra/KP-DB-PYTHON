from bank_connections import Base
from sqlalchemy import Column, Integer, String, Numeric


class ClientAccount(Base):
    __tablename__ = 'CLIENT_ACCOUNT'

    client_account_id = Column(Integer, primary_key=True)
    account_number = Column(Numeric)
    iso = Column(String(3))
    balance = Column(Numeric)
    passport_data = Column(String(20))
