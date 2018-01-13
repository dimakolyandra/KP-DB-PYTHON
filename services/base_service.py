from db_connection.connection import get_session


class BaseService:

    def __init__(self):
        self.session = get_session()
