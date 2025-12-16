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
        session.add(models.City(name="City 1"))
        session.add(models.Airport(name="Airport 1", code="A01", city_id=1))
        session.commit()

        yield session


def test_read_airport(client: TestClient):
    response = client.get("/airports/A01")
    data = response.json()
    assert response.status_code == 200, "Invalid status code"
    assert data["name"] == "Airport 1", "Invalid airport name"