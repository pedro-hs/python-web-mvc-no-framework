""" App router """


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

    def merge(self, routers):
        """ Add routes of all routers in self.routes
        :param routers Router: List of routers
        """
        for router in routers:
            self.routes.update(router.routes)
