import os
import unittest
import app

from flask import Flask, current_app
from flask_testing import TestCase


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['SECRET_KEY'] == 'generated_string')





if __name__ == '__main__':
    unittest.main()