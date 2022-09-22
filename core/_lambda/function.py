from .request import Request, Response
from ..errors import LambdaError
from ..router import router
import boto3, json, traceback


def lambda_func(handler: callable):
    def handler_wrapper(event: dict, context: dict):
        try:
            request = Request(event)
            method_handler = router.get(request.get_method())
            data, code = handler(request, method_handler)
        except LambdaError as e:
            data = "{}".format(e)
            code = e.code
        return Response(code, data).to_dict()
    return handler_wrapper


def invoke_function(name: str, 
                    payload: dict, 
                    invocation_type: str = 'RequestResponse'):
    """Invoke a Lambda function synchronously

    :param name:string: function's name, arn or partial arn
    :param payload:dict: function payload object
    :return: dict: response object
    """

    try:
        """ Convert the payload from dict -> string -> bytes 
        """
        byp = json.dumps(payload).encode()
        _client = boto3.client('lambda')
        return _client.invoke(FunctionName=name,
                              InvocationType=invocation_type,
                              LogType='Tail',
                              Payload=byp)
    except Exception:
        traceback.format_exc()
    return None