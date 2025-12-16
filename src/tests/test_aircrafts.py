import models
from db import Base
from config import get_settings

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


@pytest.fixture(name="session", scope="module")
def session_fixture():
    engine = create_engine(get_settings().DATABASE_URL)
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        session.add(
            models.Aircraft(tail_number="TS-0001", model="Test 1", fuel_per_hour=1000, total_seats=2)
        )
        session.commit()

        yield session


def test_read_aircraft(client: TestClient):
    response = client.get("/aircrafts/TS-0001")
    data = response.json()
    assert response.status_code == 200, "Invalid status code"
    assert data["model"] == "Test 1", "Invalid aircraft name"