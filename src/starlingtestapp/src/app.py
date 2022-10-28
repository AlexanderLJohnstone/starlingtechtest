from path import RequestBuilder
from user import User
import exceptions as e
import json

QUERY_STRING_PARAMETERS = 'queryStringParameters'
HEADERS = 'headers'
AUTH = 'Authorization'
DATE = 'date'
SAVINGS_ID = 'savingsGoalUid'
SAVINGS_GOALS_LIST = "savingsGoalList"
HTTP_METHOD = 'httpMethod'
PUT = 'PUT'
PATH = 'path'
ROUND = '/round'
CLI_ERR_STATUS = 400

def error_dict(error):
    """Returns dictionary form of error"""
    return {"error":error}

def get_inputs(event):
    """ Function to parse event into inputs

    Args:
        event (json): event from API Gatewau

    Returns:
        inputs : return auth toke, date for round up and savings goal ID (UUID)
    """
    try:
        auth = event[HEADERS][AUTH]
        date_input = event[QUERY_STRING_PARAMETERS][DATE]
    except:
        raise e.InputException()
    try:
        savingsGoalUid = event[QUERY_STRING_PARAMETERS][SAVINGS_ID]
    except:
        savingsGoalUid = None
    return auth, date_input, savingsGoalUid

def json_encoder(response):
    """ Uses json lib to encode response from XML """
    return json.loads(response.data.decode('utf-8'))


def lambda_handler(event, context):
    """ AWS Lambda entry point - handles orchestration of API request and round up
    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

    context: object, required
        Lambda Context runtime methods and attributes
    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict
    """
    path_builder = RequestBuilder()
    response = path_builder.response_builder(200, "")
    try:
        # Get Input from API Gateway Event
        if event[PATH] != ROUND:
            raise e.PathException(event[PATH])
        if event[HTTP_METHOD] != PUT:
            raise e.MethodException(event[HTTP_METHOD])
        auth, date, savingsGoalUid = get_inputs(event)

        call_user = User(auth, savingsGoalUid)                                      # Create User
        account_response = path_builder.send_account_request(call_user.get_auth())  # Get account info
        call_user.parse_account(json_encoder(account_response))                     # Parse account information

        # Get list of transactions for date period
        transaction_response = path_builder.send_transaction_request(auth, call_user.get_accountUid(), call_user.get_default_category(), date)
        # Calculate round up
        round_up = call_user.round_up_transactions(json.loads(transaction_response.data.decode('utf-8')))
        # Get savings goals
        savings_goals = path_builder.send_get_savings_request(auth, call_user.get_accountUid())
        num_goals = len(json.loads(savings_goals.data.decode('utf-8'))[SAVINGS_GOALS_LIST])
        
        if call_user.get_savingsGoalUid() is None:  # Create or find savingsGoalUid
            goal_response = path_builder.get_savingsGoalUid(num_goals, call_user.get_auth(), call_user.get_accountUid(), call_user.get_currency())
            call_user.set_savingsGoalUid(json_encoder(goal_response)[SAVINGS_GOALS_LIST][0]['savingsGoalUid'])
        else: # Call to verify provided goal exist
            call_user.search_savings_goals(json_encoder(savings_goals)[SAVINGS_GOALS_LIST], call_user.get_savingsGoalUid())


        # Make transfer request of round up and return status code & message from the response
        transfer_response = path_builder.send_transfer_round_up_request(auth, call_user.get_accountUid(), call_user.get_savingsGoalUid(), call_user.get_currency(), round_up)
        response = path_builder.response_builder(transfer_response.status, json_encoder(transfer_response))
   
    # Handle exceptions and return respnse
    except e.DateFormatException as exc:
        response = path_builder.response_builder(CLI_ERR_STATUS, error_dict(exc.message))
    except e.GoalNotFoundException as exc:
        response = path_builder.response_builder(CLI_ERR_STATUS, error_dict(exc.message))
    except e.PathException as exc:
        response = path_builder.response_builder(405,  error_dict(exc.message))
    except e.AccountException as exc:
        response = path_builder.response_builder(exc.response.status, json_encoder(exc))
    except e.InputException as exc:
        response = path_builder.response_builder(CLI_ERR_STATUS, error_dict(exc.message))
    except e.MethodException as exc:
        response = path_builder.response_builder(CLI_ERR_STATUS, error_dict(exc.message))
    return response


# lambda_handler(0,0)
# Put a DB in the back
# users can submit their name, a secret key and there auth token, auth tokens hard to find and no one wants to remember
# Check user exists for put!
# Add a delete?
# what if two names the same? maybe use unique usernames!
#
# Given a user get all of there accounts or maybe just primary
# access their default category online for a week period (mondays only), user should be able to suplpy any date and it'll get the week surrounding it
# perform round up calculation (trasactions out only etc)
#
# Have a class for a user, store things like category ID, auth, accountID
# Have a class for building URLs?
# Have a class for parsing response?
# Long ReadMe required
# Explain assumptions
# could have split out into multiple lambdas but creates messy architecture and increases cold-starts.
# What if no transactions?
# other currencies?
# if user does not have a goal create a default goal, otherwise add to first goal
# user can provide a goal, if none is provided we will add to it
# balance check performed by put request to API so we can just pass back error
# could look for a savings goal less than 0%
# Logging?
# NOTE THAT A CHANGE WAS MADE MID DEV TO API!!!
# TODO  test, write up read me,
# Potential problems, incorrect auth, date or savingsGoalUid. 