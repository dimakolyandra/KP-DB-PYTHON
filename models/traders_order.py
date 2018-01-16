from datetime import datetime

from db_connection.connection import Base
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

from models.trader_account import TraderAccount
from models.trading_contract import TradingContract


class TradersOrder(Base):
    __tablename__ = 'TRADERS_ORDER'

    traders_order_id = Column(Integer, primary_key=True)
    date_begin = Column(Date, default=datetime.now())
    value = Column(Numeric)
    status = Column(String(100), default='OPEN')
    date_end = Column(Date)
    first_account_id = Column(
        Integer, ForeignKey('TRADER_ACCOUNT.trader_account_id'))
    second_account_id = Column(
        Integer, ForeignKey('TRADER_ACCOUNT.trader_account_id'))
    trading_contract_id = Column(
        Integer, ForeignKey('TRADING_CONTRACT.trading_contract_id'))

    sell_account = relationship(
        TraderAccount,
        lazy='joined',
        backref='sell_orders',
        foreign_keys=[first_account_id]
    )

    bought_account = relationship(
        TraderAccount,
        lazy='joined',
        backref='bought_orders',
        foreign_keys=[second_account_id]
    )

    contract = relationship(
        TradingContract,
        lazy='joined',
        backref='orders',
        foreign_keys=[trading_contract_id]
    )
