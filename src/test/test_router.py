""" router.py test """
import inspect
import os
import sys
import unittest

# TODO: Improve path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))  # noqa isort:skip
parentdir = os.path.dirname(currentdir)  # noqa isort:skip
sys.path.insert(0, parentdir)   # noqa isort:skip


from router import Router  # noqa isort:skip
from errors import NotFound, InternalServerError  # noqa isort:skip


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
