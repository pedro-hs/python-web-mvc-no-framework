from wsgiref.simple_server import make_server

from app import App
from customers import router as customers_router
from router import Router

router = Router()
router.merge([customers_router])

HOST = 'localhost'
PORT = 8100


def main():
    """ Execute server """
    app = App(router)

    with make_server(HOST, PORT, app) as server:
        server.serve_forever()


main()
