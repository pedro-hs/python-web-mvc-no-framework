""" WSGI app """
from errors import NotFound


class App(object):
    """ WSGI app """

    def __init__(self, router):
        self.router = router

    def __call__(self, environ, start_response):
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
