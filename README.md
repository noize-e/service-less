# service-less

## 1. Overview

When I started developing apps with a serverless microservices architecture, I wasn't aware of its complexity.  So for my mental health and to make my life much easier, I created this library. 

Based on the template provided in the AWS lambda function documentation, the library provides a simple interface for the main handler function, with the capability to perform different business logic depending on the request method.

Other capabilities and features provided are:

1. One or more settings reading from a custom configuration file.
2. An access control system is provided, which validates by a whitelist if the request method is allowed.
3. Extracts and encodes from the event source(a JSON document sent from the trigger source, like AWS API Gateway) the payload body.
4. C.O.R.S headers validation:
    - Content-Type
    - X-Amz-Date
    - Authorization
    - X-Api-Key
    - x-requested-with
5. Maps the response data to the correct schema.
6. Returns a standard application/json response on an error/exception.

## 2. Getting started

### Configuration

The following list the available settings:

- HTTP_METHODS - _default: `['GET', 'POST', 'PUT', 'DELETE', 'HEAD']`_
- HTTP_CONTENT_TYPE - _default: `'application/json'`_
- CORS_HEADERS - _default: `['Content-Type', 'X-Amz-Date', 'Authorization', 'X-Api-Key', 'x-requested-with']`_
- CORS_ORIGINS - _default: `'*'`_
- CORS_X_REQUEST - _default: `'*'`_

### Request Routing

Import the __route__ deocorator.

```python
from svrless import route
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
def get_handler():
    return ("Hello World", 200)
```

__POST request__.

```python
@route
def post_handler(payload):
    return ("Hello World", 200)
```

> __NOTE!__ The expected response object must be a tuple of is a tuple `(JSON-serializable-object, int(HTTP-code[2xx, 4xx, 5xx]))`.

This is the only step needed for the method handler. The system registers the function and calls it on runtime.

### Main Handler Function

Import the __lambda_func__ deocorator.

```python
from svrless import route, lambda_func
```

For this function implement as following using the __lambda_func__ decorator. A request(event source) object and the request method handler function are passed as arguments.

For example, for a post request, we can pass the body payload b

```python
@lambda_func
def lambda_handler(request, handler):
    if request.is_post():
        return handler(request.get_payload())
    return handler()
```

## 3. Test

In a new file __`test.py`__ add the following code:

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

Then execute __`python test.py`__. 

__output:__

```console
{
    "statusCode": 200,
    "body": "{...}",
    "headers":
    {
        "X-Requested-With": "*",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,HEAD",
        "Content-Type": "application/json"
    }
}
```
