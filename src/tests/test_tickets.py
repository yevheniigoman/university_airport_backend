import models
from db import Base
from config import get_settings

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
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
            models.Seat(aircraft_id=1, seat_number="A2", seat_class=2),
            models.Seat(aircraft_id=1, seat_number="A3", seat_class=1),
            models.Seat(aircraft_id=1, seat_number="A4", seat_class=2),
            models.Seat(aircraft_id=1, seat_number="A5", seat_class=1),
            models.Seat(aircraft_id=1, seat_number="A6", seat_class=2))
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


@pytest.fixture(name="tickets_client", scope="module")
def tickets_client_fixture(client: TestClient):
    client.post(
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
    yield client

    client.delete("/flights/TS001")


def test_buy_ticket(tickets_client: TestClient):
    response = tickets_client.post(
        "/tickets/",
        json={
            "flight_number": "TS001",
            "seat_number": "A1",
            "first_name": "Bob",
            "last_name": "Smith"
        }
    )
    assert response.status_code == 200


def test_buy_already_reserved_ticket(tickets_client: TestClient):
    tickets_client.post(
        "/tickets/",
        json={
            "flight_number": "TS001",
            "seat_number": "A2",
            "first_name": "Bob",
            "last_name": "Smith"
        }
    )
    response = tickets_client.post(
        "/tickets/",
        json={
            "flight_number": "TS001",
            "seat_number": "A2",
            "first_name": "Alex",
            "last_name": "Williams"
        }
    )
    assert response.status_code == 404


def test_buy_ticket_invalid_seat(tickets_client: TestClient):
    response = tickets_client.post(
        "/tickets/",
        json={
            "flight_number": "TS001",
            "seat_number": "A10",
            "first_name": "Alex",
            "last_name": "Williams"
        }
    )
    assert response.status_code == 404