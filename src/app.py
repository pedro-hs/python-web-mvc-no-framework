""" WSGI app """
import http.client

from errors import NotFound


def handle_errors(callback):
    """ Decorator. Handle request errors
    :param callback function: callback
    """
    def wrapper(*args):
        start_response = args[2]

        try:
            return next(callback(*args))

        except NotFound:
            start_response('404 NOT FOUND', [('Content-type', 'text/html')])
            return ['Not Found'.encode()]

        except Exception as error:
            start_response('500 INTERNAL SERVER ERROR', [('Content-type', 'text/html')])
            return ['Internal Server Error'.encode()]

    return wrapper


class App(object):
    """ WSGI app
    :param router Router: App router
    """

    def __init__(self, router):
        self.router = router

    @handle_errors
    def __call__(self, environ, start_response):
        """ Callback to execute app business logic
        :param environ dict: Wsgi environ
        :param start_response function: Wsgi start_response
        :returns: Yield response body or errors
        """
        controller = self.router.get_controller(environ.get('PATH_INFO'), environ.get('REQUEST_METHOD'))
        body, status, header = self.__run_controller(controller)
        start_response(status, header)

        if body:
            yield [body.encode()]

    def __run_controller(self, controller):
        """ Execute controller
        :param controller function: Execute request operation
        :returns: Body, status, header
        """
        response = controller()
        status = self.__handle_status(response)
        header = [('Content-type', 'text/html')]
        body = response.get('body')

        return body, status, header

    def __handle_status(self, response):
        """ Process http status
        :param response dict: Response body, status. Example={'body': '[]', 'status': '204'}
        :returns: Status. Example='200 OK'
        """
        status = int(response.get('status', '200'))
        status_message = http.client.responses.get(status, 'INTERNAL SERVER ERROR')

        if status_message == 'INTERNAL SERVER ERROR':
            status = 500

        return f'{status} {status_message}'
