""" WSGI app """
from errors import NotFound


class App(object):
    """ WSGI app
    :param router Router: App router
    """

    def __init__(self, router):
        self.router = router

    def __call__(self, environ, start_response):
        """ Callback to execute app business logic
        :param environ dict: wsgi environ
        :param start_response function: wsgi start_response
        :returns: yield response body or errors
        """
        try:
            controller = self.router.get_controller(environ.get('PATH_INFO'), environ.get('REQUEST_METHOD'))
            response = controller()
            status = response.get('status', '200 OK')
            header = [('Content-type', 'text/html')]
            start_response(status, header)
            body = response.get('body')

            if body:
                yield body.encode()

        except NotFound:
            start_response('404 NOT FOUND', [('Content-type', 'text/html')])
            yield 'Not Found'.encode()

        except Exception:
            start_response('500 INTERNAL SERVER ERROR', [('Content-type', 'text/html')])
            yield 'Internal Server Error'.encode()
