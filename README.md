# service-less

## 1. Overview

When I started developing apps with a serverless microservices architecture, I wasn't aware of its complexity.  So for the sake of my mental health, I created this library. Based on the template provided by the AWS lambda function documentation, it consist of a simple interface for the main handler function. With the capability to execute a business logic per request method.

Other features are:

1. One or more settings reading from a custom configuration file.
2. Request method whitelist through an access control system.
3. Payload body parsing from the event source (a JSON document sent from the trigger source, like AWS API Gateway).
4. C.O.R.S headers validation.
5. Response data mapping to the corresponding resource schema.
6. Standard application/json response on a error/exception.

# 2. Getting started

### Configuration

The following list the available settings:

- HTTP_METHODS - _default: `['GET', 'POST', 'PUT', 'DELETE', 'HEAD']`_
- HTTP_CONTENT_TYPE - _default: `'application/json'`_
- CORS_HEADERS - _default: `['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'x-requested-with']`_
- CORS_ORIGINS - _default: `'*'`_
- CORS_X_REQUEST - _default: `'*'`_

C.O.R.S headers:

- Content-Type
- X-Amz-Date
- Authorization
- X-Api-Key
- x-requested-with

### Request Routing

Import the __route__ deocorator.

```python
from service_less import route
```

Then, define a handler function for each CRUD operation business logic with the __route__ decorator.

Following the naming convention __`{http-method}_handler()`__, changing the `{http-method}` for any in the whitelist. For example:

In a new file named `config.py` whitelist the GET and POST methods.

```python
HTTP_METHODS=['GET', 'POST']
```

Then define in the `main.py` define the handler functions:

__GET request__.

```python
@route
def get_handler() -> tuple:
    return ("Hello World", 200)
```

__POST request__.

```python
@route
def post_handler(path, payload: object) -> tuple:
    return ({"post_response": f"Request from '{path}' with payload '{payload}'"}, 200)
```

> __NOTE!__ The expected response object must be a tuple of is a tuple `(JSON-serializable-object, int(HTTP-code[2xx, 4xx, 5xx]))`.

This is the only step needed for the method handler. The system registers the function and calls it on runtime.

### Main Handler Function

Import the __lambda_func__ function and decorate the main handler function. The decorator receives 2 arguments: the __request event object__ and the __method handler function__.

```python
from service_less import route, lambda_func

...

@lambda_func
def lambda_handler(request, handler_func):
    if request.is_post():
        return handler_func(request.get_payload())
    return handler_func()
```

# 3. Test

In a new file __`test.py`__ add the following code:

### POST request Test

```python
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
        "Access-Control-Allow-Headers": "Content-Type, ...",
        "Access-Control-Allow-Methods": "GET,POST",
        "Content-Type": "application/json"
    }
}
```
