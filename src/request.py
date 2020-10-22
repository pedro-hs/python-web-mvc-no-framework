
import http.client

from errors import InternalServerError, NotFound


class Request:

    def get_service(self, environ):
        """ Get service using request informations
        :param environ dict: wsgi environ
        :returns: request service 
        :raises: NotFound or InternalServerError
        """
        url = environ.get('PATH_INFO')
        http_method = environ.get('REQUEST_METHOD')

        try:
            url = self.handle_url(url)
            service = self.routes[(http_method, url)]

        except KeyError:
            raise NotFound

        except Exception:
            raise InternalServerError

        return service

    def handle_url(self, url):
        """
        TODO
        """
        return f"/{url.split('/')[-1]}"

    def run_service(self, service, environ):
        """ Execute service
        :param service function: execute request operation
        :returns: body, status, header
        """
        response = service()
        status = self.handle_status(response)
        header = [('Content-type', 'text/html')]
        response_body = response.get('body')

        return response_body, status, header

    def handle_status(self, response):
        """ Process http status
        :param response dict: response body, status. Example={'body': '[]', 'status': '204'}
        :returns: status. Example='200 OK'
        """
        status = int(response.get('status', '200'))
        status_message = http.client.responses.get(status, 'INTERNAL SERVER ERROR')
        status = 500 if status_message == 'INTERNAL SERVER ERROR' else status

        return f'{status} {status_message}'

    @handle_errors
    def process(self, environ, routes):

        service = self.router.get_service(environ)
        return self.run_service(service, environ)

    def handle_errors(callback):  # pylint: disable=no-self-argument
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

            except Exception:
                start_response('500 INTERNAL SERVER ERROR', [('Content-type', 'text/html')])
                return ['Internal Server Error'.encode()]

        return wrapper
