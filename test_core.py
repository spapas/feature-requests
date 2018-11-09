from flask_testing import TestCase
from flask import url_for
from core import app, db
import unittest
from core.models import FeatureRequest, Client, ProductArea
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
    def test_listpage(self):
        response = self.client.get(url_for("feature_requests_view"))
        assert b"No feature requests found." in response.data
        response = self.client.get(url_for("feature_requests_view"))
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
        assert (
            url_for("feature_requests_update", feature_request_id=1).encode()
            in response.data
        )
        assert (
            url_for("feature_requests_delete", feature_request_id=1).encode()
            in response.data
        )


class CreatepageTest(BaseTest):
    def test_createpage(self):
        response = self.client.get(url_for("feature_requests_create"))
        assert b"Add Feature Request" in response.data
        assert b"<form method='POST'>" in response.data
        assert b"form-group has-error" not in response.data

        response = self.client.post(url_for("feature_requests_create"), data=dict(
            title="Title",
            description="Desc",
            client=None,
            client_priority=1,
            target_date=datetime.date(2018, 1, 1),
            product_area=None,
        ))

        assert b"form-group has-error" in response.data
        assert b"<form method='POST'>" in response.data
        assert response.status == '200 OK'

        client = Client("C1")
        db.session.add(client)
        product_area = ProductArea("PA1")
        db.session.add(product_area)
        db.session.commit()
        response = self.client.post(url_for("feature_requests_create"), data=dict(
            title="Title",
            description="Desc",
            client=client.id,
            client_priority=1,
            target_date=datetime.date(2018, 1, 1),
            product_area=product_area.id,
        ))
        assert response.status == '302 FOUND'

        response = self.client.post(url_for("feature_requests_create"), data=dict(
            title="Title",
            description="Desc",
            client=client.id,
            client_priority=1,
            target_date=datetime.date(2018, 1, 1),
            product_area=product_area.id,
        ), follow_redirects=True)
        assert response.status == '200 OK'
        assert b"Feature request created!" in response.data
        assert response.data.count(b'Update') == 2
        assert response.data.count(b'Delete') == 2
        assert client.name.encode() in response.data
        assert product_area.name.encode() in response.data


if __name__ == "__main__":
    unittest.main()
