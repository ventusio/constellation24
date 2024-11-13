import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlmodel import Session, create_engine
from testcontainers.postgres import PostgresContainer

# isort : off
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.config import Settings, get_settings  # noqa
from src.main import app  # noqa
from src.postgis import database_url  # noqa


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


@pytest.fixture(autouse=True)
def clear_reports(test_app):
    engine = create_engine(database_url, echo=True)

    # Clear all reports
    with Session(engine) as session:
        session.exec(text("DELETE FROM reports"))
        session.commit()


@pytest.fixture
def client(test_app):
    return TestClient(test_app)
