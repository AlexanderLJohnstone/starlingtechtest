# starlingtestapp - Alexander (Sandy) Johnstone Submission

## Design
For this challenge I decided to implement an API in AWS. AWS is the leading cloud provider and more and more companies are migratnig to it. Specifically, I have utilised AWS Lambdas with an API Gateway. I chose to do it this way for a number of reasons. The first is that a round up is a simple calculation. It does not require a server to be running 24/7. Round ups are also not called frequently. Most likely once per week per user, another reason not to run a server. With this in mind a lambda function makes more sense, as it can be quiclly spun up and executed when needed. I decided to use python for this challenge as I wanted to develop quickly and reduce boiler plate code. 
I could have split this into several lambdas and used step functions to orchestrate them but if done too often a code base becomes very messy (when you have a very extensive API). Lambdas should be of sufficient size so that they can make use of warm-starts (when a request is made and an existing lambda hasn't been spun down yet, the API Gateway can re-use it)

![diagram](https://d2908q01vomqb2.cloudfront.net/1b6453892473a467d07372d45eb05abc2031647a/2017/08/17/1.png)

## Code
The lambda function is invoked by the gateway passing an event and a context to the lambda_handler function inside app.py. The general flow of the code is as follows:
- Check Input
- Attempt account request to Starling API
- Get primary account and other user info
- Get transactions from that account
- Calculate round up
- If no spaceUid is provided, create one or find one
- Make transfer from primary account
Originally I also made a check of the Balance but the transfer api provides an error message if there are insufficient funds which was more convenient.

The flow/control of the program is in app.py
User class is used to encapsulate functions and attributes related to the user, like account information, transaction list, round up functionality, etc
Path Builder class in Path encapsulates URLs and functions used to build and send requests to the Starling API
Exceptions holds custom exceptions to help effectivley handle exceptions and provide meaningful error messages for the API.

This project contains supporting files for a serverless application that you can deploy with the AWS SAM CLI:

- events - Invocation events that you can use to invoke the function in lambda console.
- tests - Tests for the application code. 
- template.yaml - A template that defines the application's AWS resources.

## Assumptions
Below are assumptions I have made
- Transactions are only counted from the Primary account, as such I only use the default category as well
- Only round up outgoing transactions that have been settled
- Do not filter by counterparty. I would expect bank transfers don't count in round ups but this was not mentioned in the spec.

## API usage
The api takes two parameters:
      Date=YYYY-MM-DD
      Authorization={authorisation token for sandbox customer}
The API will take midnight from the day supplied to midnight of a week later as the transaction window.
Example
https://zg24vmagbh.execute-api.us-east-1.amazonaws.com/Prod/round?date=2022&Authorization=d93h4pfsdch-cspdhsdiuchspd9

curl -X PUT "https://zg24vmagbh.execute-api.us-east-1.amazonaws.com/Prod/round?date=2022-10-20&Authorization=dsvsbdv-sfkvsbd"


## Limitations
Below are a number of Limitations
- If a user makes a round up request to the same date twice the API does not check to see if one has already been done. It will just perform another round up.
- If 

## Testing
Testing of this application can be done locally using docker however I have implemented it so you can see a call to the API gateway. You can run this using AWS client that will automatically find your stack url (in case it changes). But for ease of use I've hard coded the URL for you.
The API is, and will continue to run, at https://zg24vmagbh.execute-api.us-east-1.amazonaws.com/Prod/round 
To run the tests you must use pylint from the starlingtestapp directory:

URL="{url}" AUTH="{Starling Sandbox customer auth}" python -m pytest tests/integration -v

URL="https://zg24vmagbh.execute-api.us-east-1.amazonaws.com/Prod/round" AUTH="{}" python3 -m pytest tests/integration -vv


## Extensions
Due to the nature of a take home challenge I decided to timebox my solution to prevent it getting out of hand. Below are a number of extensions I would add to this implementation if I had spent more time on the challenge.
- The implementation I have gone for is intended to just work. If no savingsUid is provided, the API will try to find one, and if it cannot it will create one. This isn't inkeeping with segregation of duties.

## deployment

If you have the SAM CLI and an AWS account, then you can deploy it yourself and play with it in the console:

sam deploy --guided
