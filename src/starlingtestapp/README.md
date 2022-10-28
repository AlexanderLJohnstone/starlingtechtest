# starlingtestapp



The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS Toolkit.  
The AWS Toolkit is an open source plug-in for popular IDEs that uses the SAM CLI to build and deploy serverless applications on AWS. The AWS Toolkit also adds a simplified step-through debugging experience for Lambda function code. See the following links to get started.

* [CLion](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [GoLand](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [WebStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [Rider](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PhpStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [RubyMine](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [DataGrip](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
starlingtestapp$ sam build --use-container
```

The SAM CLI installs dependencies defined in `hello_world/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
starlingtestapp$ sam local invoke HelloWorldFunction --event events/event.json
```

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
starlingtestapp$ sam local start-api
starlingtestapp$ curl http://localhost:3000/
```

The SAM CLI reads the application template to determine the API's routes and the functions that they invoke. The `Events` property on each function's definition includes the route and method for each path.

```yaml
      Events:
        HelloWorld:
          Type: Api
          Properties:
            Path: /hello
            Method: get
```

## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
starlingtestapp$ sam logs -n HelloWorldFunction --stack-name starlingtestapp --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Tests

Tests are defined in the `tests` folder in this project. Use PIP to install the test dependencies and run tests.

```bash
starlingtestapp$ pip install -r tests/requirements.txt --user
# unit test
starlingtestapp$ python -m pytest tests/unit -v
# integration test, requiring deploying the stack first.
# Create the env variable AWS_SAM_STACK_NAME with the name of the stack we are testing
starlingtestapp$ AWS_SAM_STACK_NAME=<stack-name> python -m pytest tests/integration -v
```

## Cleanup

```bash
aws cloudformation delete-stack --stack-name sta

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
https://zg24vmagbh.execute-api.us-east-1.amazonaws.com/Prod/round/roundup?date=2022&Authorization=d93h4pfsdch-cspdhsdiuchspd9

## Limitations
Below are a number of Limitations
- If a user makes a round up request to the same date twice the API does not check to see if one has already been done. It will just perform another round up.
- If 

## Testing
Testing of this application can be done locally using docker however I have implemented it so you can see a call to the API gateway.
The API is, and will continue to run, at https://zg24vmagbh.execute-api.us-east-1.amazonaws.com/Prod/round 
To run the tests you must use pylint from the root directory:
AWS_SAM_STACK_NAME="{name of deployed stack}" AUTH="{Starling Sandbox customer auth}" python -m pytest tests/integration -v
AWS_SAM_STACK_NAME="StarlingTechTestStack" AUTH="" python3 -m pytest tests/integration -vv



## Extensions
Due to the nature of a take home challenge I decided to timebox my solution to prevent it getting out of hand. Below are a number of extensions I would add to this implementation if I had spent more time on the challenge.
- The implementation I have gone for is intended to just work. If no savingsUid is provided, the API will try to find one, and if it cannot it will create one. This isn't inkeeping with segregation of duties.
