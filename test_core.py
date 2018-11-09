from flask_testing import TestCase
from flask import url_for
from core import app, db
import unittest
from core.models import FeatureRequest
import datetime


class BaseTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True

    def create_app(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class HomepageTest(BaseTest):
    def test_homepage(self):
        response = self.client.get(url_for("home_view"))
        assert b"Add a feature request:" in response.data
        assert b"List feature requests:" in response.data


class ListpageTest(BaseTest):
    def test_1_listpage_empty(self):
        response = self.client.get(url_for("feature_requests_view"))
        assert b"No feature requests found." in response.data

    def test_2_add_feature_request(self):
        fr = FeatureRequest(
            title="Title",
            description="Desc",
            client=None,
            client_priority=1,
            target_date=datetime.date(2018, 1, 1),
            product_area=None,
        )
        db.session.add(fr)
        db.session.commit()
        response = self.client.get(url_for("feature_requests_view"))
        assert b"Update" in response.data
        assert (
            url_for("feature_requests_update", feature_request_id=1).encode()
            in response.data
        )
        assert b"Delete" in response.data
        assert (
            url_for("feature_requests_delete", feature_request_id=1).encode()
            in response.data
        )

    def test_3_add_more_feature_requests(self):
        fr = FeatureRequest(
            title="Title",
            description="Desc",
            client=None,
            client_priority=1,
            target_date=datetime.date(2018, 1, 1),
            product_area=None,
        )
        db.session.add(fr)
        fr2 = FeatureRequest(
            title="Title",
            description="Desc",
            client=None,
            client_priority=1,
            target_date=datetime.date(2018, 1, 1),
            product_area=None,
        )
        db.session.add(fr2)
        db.session.commit()
        response = self.client.get(url_for("feature_requests_view"))
        assert response.data.count(b'Update') == 2
        assert response.data.count(b'Delete') == 2


if __name__ == "__main__":
    unittest.main()
