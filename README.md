# svrless

Python lib for serverless microservices.

## Usage

```python
from svrless import lambda_func, route


@route
def get_handler():
	pass


@route
def post_handler(payload):
	return ("Hello World", 200)



@lambda_func
def lambda_handler(request, handler):
	if request.is_post():
		return handler(request.get_payload())
	return handler()

```

## Test

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

output:

```python
{'statusCode': 200, 'body': '{"message": "Hello World"}', 'headers': {'X-Requested-With': '*', 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with', 'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,HEAD', 'Content-Type': 'application/json'}}
```
