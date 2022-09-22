from .errors import InvalidRouterHandler
from .config import config_attr


class Router(object):

	def __init__(self):
		self.routes = {}

	def add(self, func: callable):
		name = func.__name__
		name = name.split('_')
		verb = name[0].upper()

		try:
			name.index('handler')
		except ValueError:
			raise InvalidRouterHandler('allowed naming: {HTTP_VERB.lower}_handler')

		if verb not in config_attr("http_methods"):
			raise InvalidRouterHandler(f"method not allowed: {verb}")

		self.routes[verb] = func

	def get(self, method: str):
		return self.routes[method]


router = Router()
route = router.add