from db_connection.connection import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from models.broker_firm import BrokerFirm


class User(Base):
    __tablename__ = "USER_SYSTEM"

    user_system_id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    second_name = Column(String(100))
    birthday = Column(Date)
    phone_number = Column(String(20))
    passport_data = Column(String(20))
    login = Column(String(100))
    password = Column(String(100))
    user_type = Column(Integer)
    broker_firm_id = Column(Integer, ForeignKey('BROKER_FIRM.broker_firm_id'))

    broker_firm = relationship(
        BrokerFirm,
        foreign_keys=[broker_firm_id],
        backref='workers'
    )
