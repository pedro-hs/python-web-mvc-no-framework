""" App server """
from wsgiref.simple_server import make_server

from app import App
from router import Router

HOST = 'localhost'
PORT = 8100


def main():
    """ Prepare and execute server """
    router = Router()
    app = App(router)

    with make_server(HOST, PORT, app) as server:
        server.serve_forever()


main()
