import pytest
from sqlmodel import create_engine, text


@pytest.fixture(scope="module")
def test_engine(postgis):
    engine = create_engine(postgis.get_connection_url(), echo=True)
    return engine


def test_postgis_extension(test_engine):
    with test_engine.connect() as connection:
        result = connection.execute(text("SELECT PostGIS_Version()"))
        assert result.scalar() is not None
