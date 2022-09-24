from ..config import config_attr
from ..encoder import MultiEncoder
from ..errors import InvalidRequestMethod
import json



CORS_HEADERS = {
    'X-Requested-With': config_attr('cors_x_request'),
    'Access-Control-Allow-Origin': config_attr("cors_origins"),
    'Access-Control-Allow-Headers': ','.join(config_attr("cors_headers")),
    'Access-Control-Allow-Methods': ','.join(config_attr("http_methods")),
    'Content-Type': config_attr("http_content_type")
}


class Response(dict):
    """ Lambda function response object """
    
    def __init__(self, code: int, body: dict, headers: dict=None, cors: bool=True):
        self._code = code
        self._body = self.__encode_body(body)
        self._headers = self.__set_headers(headers, cors)
            
    def __encode_body(self, body: object):
        if isinstance(body, dict) or isinstance(body, list):
            return json.dumps(body, cls=MultiEncoder)
        return json.dumps({'message': str(body)})

    def __set_headers(self, headers: dict, cors: bool):
        headers = headers or {}
        if cors: headers.update(CORS_HEADERS)
        return headers

    def to_dict(self):
        return {
            'statusCode': self._code,
            'body': self._body,
            'headers': self._headers
        }


class Request(object):
    """ Lambda function request object """

    def __init__(self, event):
        self._request_event = event
        self._path = event.get("path", None)
        self._method = event.get('httpMethod', None)
        self.__validate_request_method()

    def __validate_request_method(self) -> dict:
        if not self._method or self._method not in config_attr("http_methods"):
            raise InvalidRequestMethod(verb=self._method)

    @property
    def path(self):
        return self._path
    
    @property
    def method(self):
        return self._method

    def get_method(self):
        return self._method

    def is_post(self):
        return self._method == 'POST'

    def get_payload(self) -> dict:
        try:
            body = dict(json.loads(self._request_event['body']))
        except:
            body = str(self._request_event['body'])
        return body
        

