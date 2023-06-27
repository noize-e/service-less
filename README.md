# ServiceLess

A Python framework to work with micro services and AWS lambda function. 

Features:
1. Extendable configuration settings.
4. C.O.R.S headers validation.
2. HTTP Requests whitelisting.
3. Request data verification.
5  Request method function routing.
6. Exceptions handling.

| **Settings**      | **Default**                                                                         |
|-------------------|-------------------------------------------------------------------------------------|
| HTTP_METHODS      | `['GET', 'POST', 'PUT', 'DELETE', 'HEAD']`                                          |
| HTTP_CONTENT_TYPE | `'application/json'`                                                                |
| CORS_HEADERS      | `['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'x-requested-with']`  |
| CORS_ORIGINS      | _`'*'`_                                                                             |
| CORS_X_REQUEST    | _`'*'`_                                                                             |

## Requests

### Routing

For CRUD operations define a handler function using the __`@route`__ deocorator.  
The function name must include the request method as prefix ending with underscore.

```python
from service_less import route

Codes = type('Codes', (,), {
    "OK": 200
})

""" HTTP Method GET"""

@route
def get_handler() -> tuple:
    return ("Hello World", Codes.OK)


""" HTTP Method POST"""
@route
def post_handler(path: str, payload: object) -> tuple:
    return ({
        "post_response": f"Request from '{path}' with payload '{payload}'"
    }, Codes.OK)
```

Response type: __`Tuple(JSON-serializable-object{}, int(2xx | 4xx | 5xx))`

### Request Whitelist

Allow the method handler function execution by adding the method in the setting list __HTTP_METHODS__.

```python
# ./config.py
HTTP_METHODS=['GET', 'POST']
```

### Request Handler

The request is expected to came from AWS API Gateway (RESTful API). With the __`@lambda_func`__ decorator is WD

Import the __service_less.lambda_func__ decorator. This receives 2 arguments: the __request event object__ and the __method handler function__, which are sent by the API Gateway service.

```python
from service_less import route, lambda_func

...

@lambda_func
def lambda_handler(request: dict, handler_func: callable) -> tuple:
    if request.is_post():
        return handler_func(request.path,
                            request.get_payload())
    return handler_func()
```

## Testing

In a new file __`test.py`__ add the following code:

### POST request Test

```python
from main import lambda_handler


response = lambda_handler({
    "resource": "/url/path",
    "path": "/url/path",
    "httpMethod": "POST",
    "headers": {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "allow": "*",
    },
    "body": f"Hello World!"
}, {})

print(response)
```

Then execute __`python test.py`__. 

__output:__

```console
{
    "statusCode": 200,
    "body": "{\"post_response\": \"Request from '/url/path' with payload 'Hello World!'\"}",
    "headers":
    {
        "X-Requested-With": "*",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
        "Access-Control-Allow-Methods": "GET,POST",
        "Content-Type": "application/json"
    }
}
```
