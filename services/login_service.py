from getpass import getpass
from sqlalchemy.orm.exc import NoResultFound

from services.base_service import BaseService
from models import User


class LoginService(BaseService):

    def login(self):
        while True:
            try:
                usr_login = input('Введите ваш логин: ')
                usr_pass = getpass('Введите пароль:')

                user = self.session.query(
                    User).filter_by(login=usr_login, password=usr_pass).one()
                return user

            except NoResultFound:
                print("Введённые данные некоректны, попробуйте ещё раз!")
