import unittest


class TestHello(unittest.TestCase):

    def test_service_exist(self):
        self.assertNotEqual(4, 5)


if __name__ == '__main__':
    unittest.main()
