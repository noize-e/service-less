from .request import Request, Response
from ..errors import LambdaError
from ..router import router


def lambda_func(handler: callable):
    def handler_wrapper(event: dict, context: dict):
        try:
            request = Request(event)
            method_handler = router.get(request.method)
            data, code = handler(request, method_handler)
        except LambdaError as e:
            data = "{}".format(e)
            code = e.code
        return Response(code, data).to_dict()
    return handler_wrapper
