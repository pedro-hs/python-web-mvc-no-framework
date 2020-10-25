""" Request handler """
import http.client

from infrastructure.errors import InternalServerError, NotFound


class Request:

    def get_service(self, environ, routes):
        """ Get service using request informations
        :param environ dict: wsgi environ
        :returns: request service 
        :raises: NotFound or InternalServerError
        """
        url = environ.get('PATH_INFO')
        http_method = environ.get('REQUEST_METHOD')

        try:
            url = self.handle_url(url)
            service = routes[(http_method, url)]

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
        body = response.get('body')

        return body, status

    def handle_status(self, response):
        """ Process http status
        :param response dict: response body, status. Example={'body': '[]', 'status': '200'}
        :returns: status. Example='200 OK'
        """
        status = int(response.get('status', '200'))
        status_message = http.client.responses.get(status, 'INTERNAL SERVER ERROR')
        status = 500 if status_message == 'INTERNAL SERVER ERROR' else status

        return f'{status} {status_message}'

    def process(self, environ, routes):
        """
        TODO
        """
        service = self.get_service(environ, routes)
        return self.run_service(service, environ)
