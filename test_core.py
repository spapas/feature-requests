import os
import tempfile

import pytest

from core import core


@pytest.fixture
def client():
    db_fd, core.app.config['DATABASE'] = tempfile.mkstemp()
    core.app.config['TESTING'] = True
    client = core.app.test_client()

    with core.app.app_context():
        core.db.create_all()

    yield client

    os.close(db_fd)
    os.unlink(core.app.config['DATABASE'])


def test_homepage(client):
    """Start with a blank database."""

    rv = client.get('/')
    assert b'List feature requests' in rv.data
    assert b'Add a feature request' in rv.data
