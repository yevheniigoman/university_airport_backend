from models import Seat
from sqlalchemy.orm import Session

# Seats map generation
SEAT_CONFIGS = {
    "Airbus A320": ["A", "B", "C", "D", "E", "F"],
    "Boeing 737-800": ["A", "B", "C", "D", "E", "F"],
    "Embraer E190": ["A", "B", "C", "D"],
    "Airbus A330-200": ["A", "B", "C", "D", "E", "F", "G", "H"],
    "Boeing 777-300ER": ["A", "B", "C", "D", "E", "F", "G", "H", "J", "K"],
}

class AircraftService():
    def __init__(self, session: Session):
        self.session = session

    def add_seat_config(self, aircraft_model: str, letters: list[str]):
        if aircraft_model in SEAT_CONFIGS:
            raise  ValueError(f"Configuration for {aircraft_model} already exists")

        SEAT_CONFIGS[aircraft_model] = letters
        print(f"Added new seat configuration for {aircraft_model}")


    def generate_seats(self, aircraft, business_rows: int):
        if aircraft.model not in SEAT_CONFIGS:
            raise ValueError(f"No seat config found for aircraft model: {aircraft.model}")

        exists = self.session.query(Seat).filter_by(aircraft_id=aircraft.id).count()
        if exists > 0:
            raise ValueError(f"Seats for aircraft: {aircraft.model} already exists")

        letters = SEAT_CONFIGS[aircraft.model]

        seats_per_row = len(letters)
        total_seats = aircraft.total_seats
        total_rows = (total_seats + seats_per_row - 1) // seats_per_row

        seats_to_add = []

        seat_count = 0
        for row in range(1, total_rows + 1):
            for letter in letters:
                seat_number = f"{row}{letter}"
                seat_class = 1 if row <= business_rows else 2

                seats_to_add.append(
                    Seat(
                        aircraft_id=aircraft.id,
                        seat_number=seat_number,
                        seat_class=seat_class
                    )
                )
                seat_count += 1
                if seat_count == total_seats:
                    break
            if seat_count == total_seats:
                break

        self.session.add_all(seats_to_add)
        self.session.commit()

        print(f"Generated {seat_count} seats for aircraft {aircraft.model} ({aircraft.tail_number})")