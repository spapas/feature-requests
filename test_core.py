from flask_testing import TestCase
from core import app, db
import unittest
import flask_testing


class MyTest(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_homepage(self):
        response = self.client.get("/")
        assert b'Add a feature request:' in response.data
        assert b'List feature requests:' in response.data


if __name__ == '__main__':
    unittest.main()
