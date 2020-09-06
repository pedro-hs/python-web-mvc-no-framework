""" router.py test """
import unittest

from errors import InternalServerError, NotFound
from router import Router


class RouterTest(unittest.TestCase):
    def test_get_controller(self):
        # success
        router = Router()
        router.routes = {('GET', '/success'): 'test'}
        controller = router.get_controller('http://localhost:8100/success', 'GET')
        assert controller == 'test'

        # NotFound
        try:
            Router().get_controller('http://localhost:8100/invalid', 'GET')
            assert False
        except NotFound:
            assert True
        except Exception:
            assert False

        # InternalServerError
        try:
            router = Router()
            router.routes = 'invalid'
            router.get_controller('http://localhost:8100/invalid', 'GET')
            assert False
        except InternalServerError:
            assert True
        except Exception:
            assert False

    def test_call_router(self):
        router = Router()

        @router('GET', '/test')
        def mock():
            pass

        assert router.routes['/test', 'GET'].__name__ == 'mock'

    def test_merge_routes(self):
        router = Router()

        @router('GET', '/test')
        def mock():
            pass

        router2 = Router()

        @router2('GET', '/test2')
        def mock2():
            pass

        router.merge([router2])
        assert router.routes['/test', 'GET'].__name__ == 'mock'
        assert router.routes['/test2', 'GET'].__name__ == 'mock2'


if __name__ == '__main__':
    unittest.main()
