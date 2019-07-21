import unittest
from flask_testing import TestCase

from app import app

class TestURLs(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app
        
    def test_root_link(self):
        result = self.client.get('/')
        self.assertEqual(result.status_code, 200)

if __name__ == '__main__':
    unittest.main()