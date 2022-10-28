from exceptions import GoalNotFoundException
import math 

class User:
    """User class to encapsulate user infor from requests and functions related to the user
        Related functions are such as round ups and parsing account JSON
    """

    def __init__(self, auth, savingsGoalUid):
        """Constructor, set auth token and a savingsGoalUiD

        Args:
            auth (String): authorisation token
            savingsGoalUid (string): UUID of savings goal to be added to
        """
        self.__auth = auth
        self.__savingsGoalUid = savingsGoalUid

    def set_primary_account_index(self, json):
        """ Find index of primary account

        Args:
            json (dict): response from accounts request
        """
        for i in range(0, len(json['accounts'])):
            if json['accounts'][i]['accountType'] == 'PRIMARY':
                self.__primary_index = i
                break

    def parse_account(self, response):
        """ Parse account response json

        Args:
            response (json): response from accounts request
        """
        self.set_primary_account_index(response)
        self.set_accountUid(response['accounts'][self.__primary_index]['accountUid'])
        self.set_default_category(response['accounts'][self.__primary_index]['defaultCategory'])
        self.set_currency(response['accounts'][self.__primary_index]['currency'])

    def set_savingsGoalUid(self, savingsGoalUid):
        self.__savingsGoalUid = savingsGoalUid

    def set_currency(self, currency):
        self.__currency = currency

    def set_accountUid(self, accountUid):
        self.__accountUid = accountUid

    def set_default_category(self, default_category):
        self.__default_category = default_category

    def get_accountUid(self):
        return self.__accountUid

    def get_default_category(self):
        return self.__default_category

    def get_currency(self):
        return self.__currency

    def get_auth(self):
        return self.__auth

    def get_savingsGoalUid(self):
        return self.__savingsGoalUid

    def parse_transaction_out_data(self, response):
        """ Parse transactional data for outgoing and settled transactions.
        Creates an array of integers of transactiona mounts

        Args:
            response (json): json from response
        """
        self.transactions = []
        for each in response['feedItems']:
            if each['direction'] == 'OUT' and each['status'] == 'SETTLED':
                self.transactions.append(each['amount']['minorUnits'])

    def parse_balance_data(self, response):
        """ Function parses cleared balance
        Function does not use total in account

        Args:
            response (int): balance
        """
        balance = response['clearedBalance']['minorUnits']
        return balance

    def search_savings_goals(self, goal_list, savingsUid):
        """ A function to check savingsUid exists

        Args:
            goal_list (list): a list of goals the user has
            savingsUid (string): saving UUID
        """
        for each in goal_list:
            if each['savingsGoalUid'] == savingsUid:
                return True
        raise GoalNotFoundException(savingsUid)

    def round_up_transactions(self, response):
        """" Actual round up functionality

        Args:
            response (): response form Starling API

        Returns:
            _type_: _description_
        """
        self.parse_transaction_out_data(response)
        round_ups = 0
        for transaction_amount in self.transactions:
            diff = self.round(transaction_amount) - transaction_amount
            round_ups = round_ups + diff
        return round_ups        

    def round(self, x):
        """Round up to nearest 100. If a multiple of 100 then do not round up.

        Args:
            x (int): number

        Returns:
            int: rounded up number
        """
        return int(math.ceil(x / 100.0)) * 100