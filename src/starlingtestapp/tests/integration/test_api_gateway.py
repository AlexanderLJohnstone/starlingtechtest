from email import header
import os
import boto3
import pytest
import requests

"""
Make sure env variable AWS_SAM_STACK_NAME exists with the name of the stack we are going to test. 
"""


class TestApiGateway:
    
    @pytest.fixture()
    def api_gateway_url(self):
        """ Get the API Gateway URL from Cloudformation Stack outputs """
        stack_name = os.environ.get("AWS_SAM_STACK_NAME")

        if stack_name is None:
            raise ValueError('Please set the AWS_SAM_STACK_NAME environment variable to the name of your stack')

        client = boto3.client("cloudformation", region_name='us-east-1')

        try:
            response = client.describe_stacks(StackName=stack_name)
        except Exception as e:
            raise Exception(
                f"Cannot find stack {stack_name} \n" f'Please make sure a stack with the name "{stack_name}" exists'
            ) from e

        stacks = response["Stacks"]
        stack_outputs = stacks[0]["Outputs"]
        api_outputs = [output for output in stack_outputs if output["OutputKey"] == "RoundUpApi"]

        if not api_outputs:
            raise KeyError(f"RoundUpAPI not found in stack {stack_name}")

        return api_outputs[0]["OutputValue"][:-1]  # Extract url from stack outputs
    
    @pytest.fixture()
    def starling_auth(self):
        """ Get the API Gateway URL from Cloudformation Stack outputs """
        auth = os.environ.get("AUTH")

        if auth is None:
            raise ValueError('Please set the AUTH environment variable to the a users AUTH token')

        return auth # Extract url from stack outputs   
        
    def test_api_gateway_no_auth(self, api_gateway_url):
        """ Call the API Gateway endpoint and check the response for no auth """
        response = requests.put(api_gateway_url+"?date=2020")

        assert response.status_code == 400
        assert response.json() == {"error": "No auth parameter"}
        
    def test_api_gateway_no_date(self, api_gateway_url):
        """ Call the API Gateway endpoint and check the response """
        response = requests.put(api_gateway_url+"?Authorization=l")

        assert response.status_code == 400
        assert response.json() == {"error": "No date parameter"}

    def test_api_gateway_bad_auth(self, api_gateway_url):
        """ Call the API Gateway endpoint and check the response """
        response = requests.put(api_gateway_url+"?date=20&Authorization=l")

        assert response.status_code == 403
        assert response.json() == {'error': 'invalid_token', 'error_description': 'Could not validate provided access token'}
        
    def test_api_gateway_bad_date(self, api_gateway_url, starling_auth):
        """ Call the API Gateway endpoint and check the response """
        response = requests.put(api_gateway_url+"?date=20&Authorization="+starling_auth)

        assert response.status_code == 400
        assert response.json() == {'error': 'Date is not in YYYY-MM-DD'} 
        
    def test_api_gateway_correct_input(self, api_gateway_url, starling_auth):
        """ Call the API Gateway endpoint and check the response """
        response = requests.put(api_gateway_url+"?date=2022-10-20&Authorization="+starling_auth)

        assert response.status_code == 200
        assert response.json()['success'] == True
        
    def test_api_gateway_no_transactions(self, api_gateway_url, starling_auth):
        """ Call the API Gateway endpoint and check the response """
        response = requests.put(api_gateway_url+"?date=2023-10-20&Authorization="+starling_auth)

        assert response.status_code == 400
        assert response.json()['success'] == False