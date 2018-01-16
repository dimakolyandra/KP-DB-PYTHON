from db_connection.connection import Base
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from models.trading_contract import TradingContract


class TraderAccount(Base):
    __tablename__ = 'TRADER_ACCOUNT'

    trader_account_id = Column(Integer, primary_key=True)
    account_number = Column(Numeric)
    trading_contract_id = Column(
        Integer, ForeignKey('TRADING_CONTRACT.trading_contract_id'))
    curr_iso = Column(String(3), ForeignKey('CURRENCY.iso'))
    status_account = Column(Integer)

    contract = relationship(
        TradingContract,
        backref='trader_accounts',
        foreign_keys=[trading_contract_id]
    )
