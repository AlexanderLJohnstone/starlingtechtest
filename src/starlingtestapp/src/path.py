from exceptions import DateFormatException, AccountException
import urllib3
import datetime
import json
import uuid

class RequestBuilder:
    """
    This class builds requests using user data.

    The class stores all neccessary url paths and sub-paths.
    It appends input to create URLs, body data and send requests.

    Example:
    my_builer = RequestBuilder()
    response = my_builder.send_acount_request(authorization_bearer)
    response = my_builder.send_transaction_request(authorization_bearer, \
                                                    accountUid, categoryUid, start of date range)
    """
    def __init__(self):
        # Simple constructor for class to initiate paths and start a PoolManager to build requests.
        # All variables are private
        self.__account_base_path = "https://api-sandbox.starlingbank.com/api/v2/accounts"
        self.__transaction_base_path = "https://api-sandbox.starlingbank.com/api/v2/feed/account/"
        self.__savings_base_path = "https://api-sandbox.starlingbank.com/api/v2/account/"
        self.__savings_path = "/savings-goals"
        self.__transfer_path = "/add-money/"
        self.__category_path = "/category/"
        self.__transactions_path = "/transactions-between"
        self.__headers = {'Accept': 'application/json'}
        self.http = urllib3.PoolManager()

    def build_header(self, auth):
        """ Build header argument and assign to class variable

        Args:
            auth (string): Bearer Token for request authorisation
        """
        self.__headers['Authorization'] = 'Bearer ' + auth

    def send_account_request(self, auth):
        """ Send a request to account path to get a list of user accounts

        Args:
            auth (string): authorization_bearer

        Returns:
            Response: response from https request
        """
        self.build_header(auth)
        response =  self.http.request('GET',
                        self.__account_base_path,
                        headers = self.__headers,
                        retries = False)
        if response.status != 200:                  # Catch Authentication error
            raise AccountException(response)
        return response
        
    def send_account_balance_request(self, auth, accountUid):
        """ Send a request to account path to get balance

        Args:
            auth (string): authorization_bearer
            accountUid (string): UUID token for account
        Returns:
            Response: response from https request
        """
        self.build_header(auth)
        url = self.__account_base_path+ "/" + accountUid + "/balance"
        return self.http.request('GET',
                        url,
                        headers = self.__headers,
                        retries = False)

    def send_transaction_request(self, auth, accountUid, categoryUid, changes_since):
        """ This function requests a list of transactions between two dates

        Args:
            auth (string): authorization_bearer
            accountUid (string): UUID string identifying an account
            categoryUid (string): UUID string identfying a category
            changes_since (string): start of week to be rounded up

        Returns:
            Response: response from https request
        """
        self.build_header(auth)
        url = self.__transaction_base_path + accountUid + self.__category_path + categoryUid + self.__transactions_path
        url = url + "?minTransactionTimestamp=" + \
        self.time_parser(changes_since, 0).replace(":", "%3A") + \
            "&maxTransactionTimestamp=" + self.time_parser(changes_since, 7).replace(":", "%3A")

        return self.http.request('GET',
                        url,
                        headers = self.__headers,
                        retries = False)

    def build_savings_url(self, accountUid):
        """ This builds savings url
    
        Args:
            accountUid (string): UUID string identifying an account

        Returns:
            url: url for savings 
        """
        return self.__savings_base_path + accountUid + self.__savings_path

    def send_transfer_round_up_request(self, auth, accountUid, savingsGoalUid, currency, amount):
        """This functions

        Args:
            auth (string): authorization_bearer
            accountUid (string): UUID string identifying an account
            savingsGoalUid (string): UUID string identifying a savings goal
            currency (string): currency identifier e.g. GBP
            amount (int): amount to be transferred in minor units

        Returns:
            Response: response from https request
        """
        self.build_header(auth)
        url = self.build_savings_url(accountUid)
        url = url + "/" + savingsGoalUid + self.__transfer_path + str(uuid.uuid4())
        self.__headers['Content-Type'] = 'application/json'
        data = {
            "amount": {
                "currency": currency,
                "minorUnits": amount
            }
        }
        return self.http.request('PUT', url, headers = self.__headers,body=json.dumps(data),retries = False)

    def send_get_savings_request(self, auth, accountUid):
        """ This function returns a list of savings goals

        Args:
            auth (string): authorization_bearer
            accountUid (string): UUID string identifying an account

        Returns:
            Response: response from https request
        """
        self.build_header(auth)
        url = self.build_savings_url(accountUid)
        return self.http.request('GET',
                        url,
                        headers = self.__headers,
                        retries = False)

    def send_put_savings_request(self, auth, accountUid, currency):
        """ This function builds and sends a default savings goal

        Args:
            auth (string): authorization_bearer
            accountUid (string): UUID string identifying an account
            currency (string): currency identifier

        Returns:
            Response: response from https request
        """
        self.build_header(auth)
        url = self.build_savings_url(accountUid)
        data = {
            "name": "New Savings Goal",
            "currency": currency,
            
            "target": {
                "currency": currency,
                "minorUnits": 100000
            },
            "base64EncodedPhoto": "string"
            }
        self.__headers['Content-Type'] = 'application/json'
        return self.http.request('PUT',
                        url,
                        headers = self.__headers,
                        body=json.dumps(data),
                        retries = False)

    def add_days(self, date, days):
        """Add days to date and return as date"""
        return date + datetime.timedelta(days=days)

    def time_parser(self, date, addDays):
        """ Given a date and a modifier in days return a timer suitable for API request (ISO)

        Args:
            date (_type_): _description_
            addDays (_type_, optional): _description_. Defaults to None.

        Raises:
            Value Error: Raise value error if user returns a badly formatted Date

        Returns:
            date: a date in ISO format
        """
        date_split = date.split('-')
        try:
            if len(date_split) != 3:
                raise ValueError            
            new_date = self.add_days(datetime.datetime.strptime(date, "%Y-%m-%d"), addDays)
            days = new_date.day
            month = new_date.month
            year  = new_date.year
        except:
            raise DateFormatException(date)
        return datetime.datetime(year, month, days, 0, 0, 0, 000).isoformat() + ".000Z"

    def response_builder(self, status_code, body=None):
        """ Builds response message

        Args:
            status_code (int): Status code from REST API doc
            body (str): Message payload. Defaults to None.

        Returns:
            response: built response
        """
        response = {
                    'statusCode': status_code,
                    'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                    }
                }
        if body is not None:
            response['body'] = json.dumps(body)
        return response

    def get_savingsGoalUid(self, num_goals, auth, accountUid, currency):
        """If no savings ID supplied get one.
        If one exists, take first, otherwise create a new request

        Args:
            num_goals (int): number of goals user has
            auth (string): auth token
            accountUid (string): account UUID
            currency (string): currency identifier

        Returns:
            _type_: _description_
        """
        if num_goals == 0:
            self.send_put_savings_request(auth, accountUid, currency)
        return self.send_get_savings_request(auth, accountUid)
