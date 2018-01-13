import os
from services import OpenDealService, LoginService


class Main:
    def __init__(self):
        self.login_serv = LoginService()
        self.open_deal_serv = OpenDealService()

    def menu(self):
        print("Вам доступны команды:")
        print("-h - помощь")
        print("-new_deal - открыть новую сделку")
        print("-exit - выход")
        print("=" * 30)
        input("Нажмите enter, чтобы продолжить...")

    def call_operation(self, cmd, user):
        if cmd == '-h':
            self.menu()

        if cmd == '-new_deal':
            self.open_deal_serv.open_deal(user)

        if cmd == '-exit':
            exit()

    def run(self):
        user = self.login_serv.login()

        hello_str = "Здравствуйте, {} {}, вы вошли в систему!".format(
            user.first_name,
            user.second_name)

        print(hello_str)
        self.menu()

        while True:
            os.system('cls')
            cmd = input("Введите команду: ")
            self.call_operation(cmd, user)

if __name__ == "__main__":
    app = Main()
    app.run()
