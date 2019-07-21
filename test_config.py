import unittest

from flask import current_app
from flask_testing import TestCase

from app import app

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'generated_string')
        self.assertFalse(current_app is None)
        


if __name__ == '__main__':
	unittest.main()