import os
from models.broker_firm import BrokerFirm
from models.currency import Currency
from models.trading_contract import TradingContract
from services.base_service import BaseService
from settings.connection import connection_dict


class OpenDealService(BaseService):

    def __init__(self):
        super(OpenDealService, self).__init__()
        self.brokers_systems_list = self.session.query(BrokerFirm).all()
        self.trading_contracts_list = self.session.query(TradingContract).all()
        self.brokers_systems_connections = connection_dict

        currency_list = self.session.query(Currency).all()
        self.currency_dict = dict()
        for curr in currency_list:
            self.currency_dict.update({curr.iso: curr})

    def choose_currency(self, sell_or_bought):
        while True:
            try:
                print("Выберите валюту для {}:".format(sell_or_bought))
                for curr in self.currency_dict.values():
                    print(curr.currency_name + ' - ' + curr.iso)

                chosen_curr = input(
                    "Введите код валюты {}:".format(sell_or_bought))

                return self.currency_dict[chosen_curr]

            except KeyError:
                print("Некорректный ввод, введите ещё раз!")
                continue

    def find_bank_account(user, currency):
        pass

    def get_balance(user, client_account):
        pass

    def choose_broker(self, user):
        keys = [i for i in range(0, len(user.contracts))]
        values = [contract for contract in user.contracts]
        users_contract = dict(zip(keys, values))

        while True:
            try:
                print("Выберите брокера из списка тех," +
                      "с кем вы заключили договор:")
                for k in sorted(users_contract.keys()):
                    print("Чтобы вас обслуживал {} {} введите - {}".format(
                        users_contract[k].broker_user.first_name,
                        users_contract[k].broker_user.second_name,
                        k))
                    user_choice = input("Ввод: ")
                    return users_contract[int(user_choice)]
            except KeyError:
                print("Неверный ввод, попробуйте ещё раз!")

    def choose_value_and_accounts(self, user):
        pass

    def open_deal(self, user):
        try:
            while True:
                currency_sell = self.choose_currency('продажи')

                os.system('cls')

                currency_bought = self.choose_currency('покупки')

                os.system('cls')

                chosen_contract = self.choose_broker(user)

                os.system('cls')

        except:
            self.session.rollback()
