from db_connection.connection import get_session


class BaseService:
    session = get_session()
