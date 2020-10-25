""" WSGI app """
from infrastructure.request import Request
from infrastructure.router import Router


class App(object):
    """ WSGI app
    :param router Router: app router
    """

    def __init__(self, router):
        self.router = router

    def __call__(self, environ, start_response):
        """ Callback to execute app business logic
        :param environ dict: wsgi environ
        :param start_response function: wsgi start_response
        :returns: yield response body or error
        """
        body, status = Request().process(environ, self.router.routes)
        header = [('Content-type', 'text/html')]
        start_response(status, header)

        if body:
            yield [body.encode()]


def get_app():
    """ Return App configured """
    router = Router()
    app = App(router)
    return app
