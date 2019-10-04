import pytest

from notifico.app import create_app


@pytest.fixture
def app():
    return create_app()
