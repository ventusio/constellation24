import os
import sys

import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.config import Settings, get_settings  # noqa
from src.main import app  # noqa


@pytest.fixture(scope="module")
def postgis():
    with PostgresContainer("postgis/postgis:latest") as postgis:
        yield postgis


@pytest.fixture(scope="module")
def test_app(postgis):
    def get_test_settings():
        return Settings(
            db_host=postgis.get_container_host_ip(),
            db_port=postgis.get_exposed_port(5432),
        )

    app.dependency_overrides[get_settings] = get_test_settings
    return app


@pytest.fixture
def client(test_app):
    return TestClient(test_app)
