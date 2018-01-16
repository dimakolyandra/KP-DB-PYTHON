import os
import json
import requests as req
from decimal import Decimal

from models.broker_firm import BrokerFirm
from models.currency import Currency
from models.trading_contract import TradingContract
from models.traders_order import TradersOrder
from models.trader_account import TraderAccount
from services.base_service import BaseService
from settings.url import url


class OpenDealService(BaseService):

    def __init__(self):
        # super(OpenDealService, self).__init__()
        # print("AAAAAAAA")
        # print(self.session)
        self.brokers_systems_list = self.session.query(BrokerFirm).all()
        self.trading_contracts_list = self.session.query(TradingContract).all()
        # self.brokers_systems_connections = connection_dict

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

    def choose_account(self, users_accounts_dict, is_sell):
        sell_or_bought = 'продажи' if is_sell else 'покупки'
        while True:
            try:
                print("Выберите счёт для {}:".format(sell_or_bought))
                for k in sorted(users_accounts_dict.keys()):
                    print("Чтобы выбрать счёт: {}, валюта {} введите - {}"
                          .format(users_accounts_dict[k].account_number,
                                  users_accounts_dict[k].curr_iso,
                                  k))
                    chosen_account = input("Ввод: ")
                    return users_accounts_dict[int(chosen_account)]
            except KeyError:
                print("Неверный ввод, попробуйте ещё раз!")

    def find_bank_accounts(self, currency, contract):
        return self.session.query(TraderAccount).filter_by(
            curr_iso=currency.iso,
            trading_contract_id=contract.trading_contract_id).all()

    def get_users_accounts_by_currency(self, contract, currency):
        accounts = self.find_bank_accounts(currency, contract)

        if len(accounts) == 0:
            raise Exception("У вас нет соответсвующего счёта," +
                            " все изменения будут отменены!")

        keys_acc = [i for i in range(0, len(accounts))]
        values_acc = [account for account in accounts]
        return dict(zip(keys_acc, values_acc))

    def get_balance(self, user_passport, broker_firm_id, client_account):
        json_data = {
            'passport_data': user_passport,
            'broker_firm_id': str(broker_firm_id),
            'account_number': str(client_account)
        }

        ans = req.post(
            url,
            data=json.dumps(json_data),
            headers={'Content-Type': 'application/json'}
        )

        if ans.status_code == 200:
            return json.loads(ans.text)['balance']
        else:
            raise Exception()

    def is_value_valid(self, value, balance, contract):
        value_with_commission = value + value * contract.brokerage_commission
        return balance >= value_with_commission

    def choose_value_and_accounts(self,
                                  contract,
                                  currency_sell,
                                  currency_bought):
        users_sell_accounts = self.get_users_accounts_by_currency(
            contract,
            currency_sell
        )

        sell_acc = self.choose_account(users_sell_accounts, True)
        os.system('cls')

        users_bought_accounts = self.get_users_accounts_by_currency(
            contract,
            currency_bought
        )

        bought_acc = self.choose_account(users_bought_accounts, False)
        os.system('cls')

        broker_firm_id = contract.broker_user.broker_firm.broker_firm_id

        try:
            balance = self.get_balance(
                    contract.trader_user.passport_data,
                    broker_firm_id,
                    sell_acc.account_number
            )
            balance = Decimal(balance)
        except Exception:
            raise Exception("Возникла проблема на стороне банка!")

        print("Получен ответ от банка, " +
              "ваш баланс по счёту продажи составляет: {}".format(balance))

        while True:
            value = input("Введите сколько у.е. валюты продажи\n" +
                          "вы хотите обменять в пользу валюты покупки:")
            value = Decimal(value)
            if self.is_value_valid(value, balance, contract):
                return value, sell_acc, bought_acc
            else:
                print("Неправильный ввод суммы сделки, попробуйте ещё раз!")

    def submit_deal(self):
        subm = input("Подтвердите сделку: да / нет: ")
        return subm == "да"

    def open_deal(self, user):
        try:
            while True:
                currency_sell = self.choose_currency('продажи')

                os.system('cls')

                currency_bought = self.choose_currency('покупки')

                os.system('cls')

                chosen_contract = self.choose_broker(user)

                os.system('cls')

                value, sell_acc, bought_acc = self.choose_value_and_accounts(
                    chosen_contract, currency_sell, currency_bought)

                if self.submit_deal():
                    new_deal = TradersOrder()
                    new_deal.value = value
                    new_deal.status = 'OPEN'
                    new_deal.sell_account = sell_acc
                    new_deal.bought_account = bought_acc
                    new_deal.contract = chosen_contract
                    self.session.add(new_deal)
                    self.session.commit()
                    break
                else:
                    print("Открыть сделку не удалось!")
                    break

        except Exception as ex:
            print("В ходе открытия сделки возникла ошибка: " + str(ex))
            input("Нажмите enter, чтобы продолжить ...")
            self.session.rollback()
