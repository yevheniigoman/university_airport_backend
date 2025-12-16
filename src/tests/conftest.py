from main import app
from dependencies import get_session

import pytest
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

@pytest.fixture(name="client", scope="module")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
