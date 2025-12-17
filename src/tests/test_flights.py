import models
from db import Base
from config import get_settings

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from datetime import datetime


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
        session.add_all(
            (models.Seat(aircraft_id=1, seat_number="A1", seat_class=1),
            models.Seat(aircraft_id=1, seat_number="A2", seat_class=2))
        )
        session.add_all(
            (models.City(name="City 1"),
            models.City(name="City 2"))
        )
        session.add_all(
            (models.Airport(name="Airport 1", code="A01", city_id=1),
            models.Airport(name="Airport 2", code="A02", city_id=2))
        )
        session.commit()

        yield session


def test_create_flight(client: TestClient):
    response = client.post(
        "/flights/",
        json={
            "flight_number": "TS001",
            "aircraft_tail_number": "TS-0001",
            "dep_airport_code": "A01",
            "arr_airport_code": "A02",
            "departure_time": datetime(2025, 10, 12, 9, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_time": datetime(2025, 10, 13, 9, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "economy_price": "150",
            "business_price": "300",
        }
    )
    assert response.status_code == 200, "Invalid status code"


def test_create_flight_same_airports(client: TestClient):
    response = client.post(
        "/flights/",
        json={
            "flight_number": "TS001",
            "aircraft_tail_number": "TS-0001",
            "dep_airport_code": "A01",
            "arr_airport_code": "A01",
            "departure_time": datetime(2025, 10, 12, 9, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_time": datetime(2025, 10, 13, 9, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "economy_price": "150",
            "business_price": "300",
        }
    )

    assert response.status_code == 422, "Invalid status code"


def test_create_flight_departure_greater_than_arrival(client: TestClient):
    response = client.post(
        "/flights/",
        json={
            "flight_number": "TS001",
            "aircraft_tail_number": "TS-0001",
            "dep_airport_code": "A01",
            "arr_airport_code": "A01",
            "departure_time": datetime(2025, 10, 13, 9, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_time": datetime(2025, 10, 12, 9, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "economy_price": "150",
            "business_price": "300",
        }
    )

    assert response.status_code == 422, "Invalid status code"


def test_delete_flight(client: TestClient):
    response = client.delete("/flights/TS001")
    assert response.status_code == 200, "Invalid status code"