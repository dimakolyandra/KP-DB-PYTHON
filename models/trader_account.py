from db_connection.connection import Base
from sqlalchemy import Column, Integer, Numeric, ForeignKey


class TraderAccount(Base):
    __tablename__ = 'TRADER_ACCOUNT'

    trader_account_id = Column(Integer, primary_key=True)
    account_number = Column(Numeric)
    trading_contract_id = Column(
        Integer, ForeignKey('TRADING_CONTRACT.trading_contract_id'))
    curr_iso = Column(Integer, ForeignKey('CURRENCY.iso'))
    status_account = Column(Integer)
