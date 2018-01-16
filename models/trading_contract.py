from db_connection.connection import Base
from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from models.user import User


class TradingContract(Base):
    __tablename__ = 'TRADING_CONTRACT'

    trading_contract_id = Column(Integer, primary_key=True)
    trader_user_id = Column(Integer, ForeignKey('USER_SYSTEM.user_system_id'))
    broker_user_id = Column(Integer, ForeignKey('USER_SYSTEM.user_system_id'))
    brokerage_commission = Column(Numeric)

    trader_user = relationship(
        User,
        lazy="joined",
        backref='contracts',
        foreign_keys=[trader_user_id]
    )

    broker_user = relationship(
        User,
        lazy="joined",
        backref='clients_contracts',
        foreign_keys=[broker_user_id]
    )
