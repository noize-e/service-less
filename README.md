# Serviless

In building web solutions implementing a micro-service architecture using Amazon Web Services, I stumbled upon a few problems from low to high complexity. 
So, using the already defined template for lambda functions deployment, I abstract most of the functionality regarding the required implementation by the service and then can focus only on creating the business logic for the service.

## Features:

1. It has a configuration file with default values, that can be replace with one custom with the values we need to set.
4. C.O.R.S headers validation.
2. HTTP Request method filtering (whitelist).
3. Request payload body validation and format verification.
5. Response data mapping by a resource schema.
6. Errors/Eceptions standard application/json response.

## Config

#### Settings

| **Settings**      | **Default**                                                                         |
|-------------------|-------------------------------------------------------------------------------------|
| HTTP_METHODS      | `['GET', 'POST', 'PUT', 'DELETE', 'HEAD']`                                          |
| HTTP_CONTENT_TYPE | `'application/json'`                                                                |
| CORS_HEADERS      | `['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'x-requested-with']`  |
| CORS_ORIGINS      | _`'*'`_                                                                             |
| CORS_X_REQUEST    | _`'*'`_                                                                             |

#### C.O.R.S headers

- Content-Type
- X-Amz-Date
- Authorization
- X-Api-Key
- x-requested-with

## 

### Router

Create a new `config.py` and set the methods to be whitelisted.

```python
HTTP_METHODS=['GET', 'POST']
```

Create a new `main.py` file, then import the __service_less.route__ deocorator and define the handler function for each C.R.U.D. operation.
> **Note!** The name of the function follows the convention: _def_ __`{http-method}_handler()`__.

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

The response must be a tuple: `(JSON-serializable-object, int(HTTP-code[2xx, 4xx, 5xx]))`.

Now we need to connect the request's handlers and connect them with the lambda main handler function.

## Lambda Function Handler

Import the __service_less.lambda_func__ decorator. This receives 2 arguments: the __request event object__ and the __method handler function__, which are sent by the API Gateway service.

```python
from service_less import route, lambda_func

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


""" HTTP Method POST"""

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
