from flask import Flask
from flask_testing import TestCase


class BaseTestCase(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()