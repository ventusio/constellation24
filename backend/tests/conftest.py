import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.main import app  # noqa


@pytest.fixture
def client():
    return TestClient(app)
