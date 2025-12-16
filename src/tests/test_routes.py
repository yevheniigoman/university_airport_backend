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
            models.City(name="City 2"),
            models.City(name="City 3"))
        )
        session.add_all(
            (models.Airport(name="Airport 1", code="A01", city_id=1),
            models.Airport(name="Airport 2", code="A02", city_id=2),
            models.Airport(name="Airport 3", code="A03", city_id=3))
        )
        session.commit()
        yield session


@pytest.fixture(name="routes_client")
def routes_client_fixture(client: TestClient):
    client.post(
        "/flights/",
        json={
            "flight_number": "OK101",
            "aircraft_tail_number": "TS-0001",
            "dep_airport_code": "A01",
            "arr_airport_code": "A02",
            "departure_time": datetime(2025, 10, 12, 9, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_time": datetime(2025, 10, 13, 9, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "economy_price": "150",
            "business_price": "300",
        }
    )
    client.post(
        "/flights/",
        json={
            "flight_number": "OK102",
            "aircraft_tail_number": "TS-0001",
            "dep_airport_code": "A02",
            "arr_airport_code": "A03",
            "departure_time": datetime(2025, 10, 13, 11, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "arrival_time": datetime(2025, 10, 13, 15, 0, 0).strftime("%Y-%m-%d %H:%M:%S"),
            "economy_price": "150",
            "business_price": "300",
        }
    )
    yield client
    client.delete("/flights/OK101")
    client.delete("/flights/OK102")


def test_search_direct_route(routes_client: TestClient):
    response = routes_client.get("/search?from_city=City 1&to_city=City 2")
    assert response.status_code == 200, "Invalid status code"
    
    data = response.json()
    assert len(data) == 1, "Too much routes between cities 'City 1' and 'City 2'"


def test_search_route_with_one_stop(routes_client: TestClient):
    from_city_name = "City 1"
    to_city_name = "City 3"
    response = routes_client.get(f"/search?from_city={from_city_name}&to_city={to_city_name}")
    assert response.status_code == 200, "Invalid status code"

    data = response.json()
    assert len(data) == 1, "Invalid route length"

    result_route = data[0]
    result_from_city_name = result_route["flights"][0]["dep_airport"]["city"]["name"]
    assert result_from_city_name == from_city_name, "Invalid 'from_city' in route"

    result_to_city_name = result_route["flights"][-1]["arr_airport"]["city"]["name"]
    assert result_to_city_name == to_city_name, "Invalid 'to_city' in route"
