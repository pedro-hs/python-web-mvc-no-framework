""" App router """
from errors import InternalServerError, NotFound


class Router:
    """ Handle app routes
    :param routes dict: All app routes. Example={('GET', '/score'): handle_score}
    """

    def __init__(self):
        self.routes = {}

    def __call__(self, url, http_method):
        """ Decorator. Add new route to self.routes
        :param url str: Url of route. Example='/score'
        :param http_method str: Http method of route. Example='GET'
        """
        def wrapper(callback):
            route = {(http_method, url): callback}
            self.routes.update(route)

        return wrapper

    def get_controller(self, url, http_method):
        """ Get controller by route(url + http_method)
        :param url str: Route url. Example='https://localhost.com/score'
        :param http_method str: Route http method. Example='GET'
        :returns: request controller
        :raises: NotFound or InternalServerError
        """
        try:
            url = f"/{url.split('/')[-1]}"
            controller = self.routes[(http_method, url)]

        except KeyError:
            raise NotFound

        except Exception:
            raise InternalServerError

        return controller

    def merge(self, routers):
        """ Add routes of all routers in self.routes
        :param routers Router: List of routers
        """
        for router in routers:
            self.routes.update(router.routes)
