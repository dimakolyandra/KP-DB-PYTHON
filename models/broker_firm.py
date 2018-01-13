from db_connection.connection import Base
from sqlalchemy import Column, Integer, String, BLOB


class BrokerFirm(Base):
    __tablename__ = 'BROKER_FIRM'

    broker_firm_id = Column(Integer, primary_key=True)
    firm_name = Column(String(100))
    state_registration_number = Column(String(100))
    individual_taxpayer_index = Column(String(100))
    avatar = Column(String(256))
    licence = Column(BLOB)
