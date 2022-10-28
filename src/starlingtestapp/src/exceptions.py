class DateFormatException(Exception):
    """Exception raised for errors in the input date.

    Attributes:
        date -- input date which caused the error
        message -- explanation of the error
    """

    def __init__(self, date, message="Date is not in YYYY-MM-DD"):
        self.date = date
        self.message = message
        super().__init__(self.message)

class GoalNotFoundException(Exception):
    """Exception raised for errors in the savingsGoalUid.

    Attributes:
        savingsGoalUid -- input savingsGoalUid which caused the error
        message -- explanation of the error
    """

    def __init__(self, savingsGoalUid, message="SavingsGoalUid is invalid."):
        self.savingsGoalUid = savingsGoalUid
        self.message = message
        super().__init__(self.message)

        
        
class AccountException(Exception):
    """Exception raised for errors in the account call.

    Attributes:
        response -- response
        message -- explanation of the error
    """

    def __init__(self, response, message="Authorization denied."):
        self.response = response
        self.message = message
        super().__init__(self.message)
        
class InputException(Exception):
    """Exception raised for errors in the input.

    Attributes:
        inp -- input that caused an issue
    """

    def __init__(self, inp):
        self.message = inp
        super().__init__(self.message)