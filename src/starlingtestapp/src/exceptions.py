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

class PathException(Exception):
    """Exception raised for errors in the path.

    Attributes:
        path -- input path which caused the error
        message -- explanation of the error
    """

    def __init__(self, path, message="Path is invalid."):
        self.path = path
        self.message = message
        super().__init__(self.message)
        
class MethodException(Exception):
    """Exception raised for errors in the http method.

    Attributes:
        method -- method which caused the error
        message -- explanation of the error
    """

    def __init__(self, method, message="Path is invalid."):
        self.method = method
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
        message -- explanation of the error
    """

    def __init__(self, inp, message="Missing or incorrect input."):
        self.inp = inp
        self.message = message
        super().__init__(self.message)