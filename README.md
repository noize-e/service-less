# service-less

Python lib for serverless microservices development with AWS services. The lib provides a simple interface to handle http requests(C.R.U.D handler methods) coming from AWS API Gateway service, among others.

## Features

- Custom settings configuration
- HTTP Verbs whitelisting
- CORS
- DynamoDB decimal encoding
- C.R.U.D paths routing.

## Support

- Amazon API Gateway request

Comming soon:

- Amazon Cognito User Pools requests 
- SNS requests

## Usage

```python
from svrless import lambda_func, route

# Add the HTTP GET method handler
@route
def get_handler():
    pass

"""Add the HTTP POST method handler 
with the body payload as argument"""
@route
def post_handler(payload):
    return ("Hello World", 200)


"""The @lambda_func decorator perform:
1. The request event data parsing.
2. Validates the request method is whitelisted.
3. Retrieves from the router the method handler.
4. Once the logic inside the custom handler function 
   is executed it returns the required data structure 
   by the lambda's service
"""

@lambda_func
def lambda_handler(request, handler):
    if request.is_post():
        return handler(request.get_payload())
    return handler()
```

## Test

Create a new file and put in it the following code.

```python
response = lambda_handler({
    "resource": "/url/path",
    "path": "/url/path",
    "httpMethod": "POST",
    "headers": {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-xl",
        "allow": "*",
    },
    "body": "{\"key\":\"tok_434rx43xsd3\"}"
}, {})

print(response)
```

__output:__

```python
{'statusCode': 200, 'body': '{"message": "Hello World"}', 'headers': {'X-Requested-With': '*', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with', 'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,HEAD', 'Content-Type': 'application/json'}}
```
