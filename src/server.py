""" App server """
from wsgiref.simple_server import make_server

from app import get_app

HOST = 'localhost'
PORT = 8100


def main():
    """ Prepare and execute server """
    app = get_app()

    with make_server(HOST, PORT, app) as server:
        server.serve_forever()


main()
