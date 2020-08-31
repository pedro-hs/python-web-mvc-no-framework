""" App Router """
from errors import InternalServerError, NotFound


class Router:
    """ Handle app routes
    :param routes dict: All app routes
    """

    def __init__(self):
        self.routes = {}

    def __call__(self, url, http_method):
        def wrapper(function):
            route = {(http_method, url): function}
            self.routes.update(route)

        return wrapper

    def get_controller(self, url, http_method):
        """ Get controller by route
        :param url str: Route url
        :param http_method str: Route http method
        """
        try:
            controller = self.routes[http_method, url]

        except KeyError:
            raise NotFound()

        except Exception:
            raise InternalServerError()

        return controller

    def merge(self, routers):
        """ Add routes of all routers in self.routes
        :param routers Router: List of routers
        """
        for router in routers:
            self.routes.update(router.routes)
