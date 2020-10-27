import unittest
from app import app as application


class TestHello(unittest.TestCase):

    def setUp(self):
        app = application.test_client()
        self.response = app.get('/measurement')

    def test_service_exist(self):
        self.assertNotEqual(None, self.response)


if __name__ == '__main__':
    unittest.main()
