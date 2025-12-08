from models import Ticket, Flight, Seat
from datetime import datetime



class Passenger():
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name


class TicketService():
    def __init__(self, session, reservation_service):
        self.session = session
        self.reservation_service = reservation_service


    def buy(self, passenger: Passenger, flight: Flight, seat_number: str):

        # check if there are available seats
        available_seats = flight.business_available_seats + flight.economy_available_seats
        if available_seats <= 0:
            raise ValueError("There are no available seats left for this flight")

        # find seat by number
        seat = self.session.query(Seat).filter_by(aircraft_id = flight.aircraft_id, seat_number = seat_number).first()
        if not seat:
            raise ValueError(f"Seat {seat_number} does not exist on this aircraft")

        # checking if the seat has been sold
        sold_ticket = self.session.query(Ticket).filter_by(flight_id = flight.id, seat_id = seat.id, status=1).first()
        if sold_ticket:
            raise ValueError(f"Seat {seat_number} is already sold")

        # Try to reserve seat in Redis (atomic lock)
        reserved = self.reservation_service.reserve_ticket(flight.id, seat_number)

        if not reserved:
            raise ValueError(f"Seat {seat_number} is already reserved")

        if seat.seat_class == 1:
            price = flight.business_price
        else:
            price = flight.economy_price

        try:
            ticket = Ticket(
                flight_id = flight.id,
                seat_id = seat.id,
                first_name = passenger.first_name,
                last_name = passenger.last_name,
                purchase_date = datetime.now(),
                price = price,
                status = 1
            )

            self.session.add(ticket)

            if seat.seat_class == 1:
                flight.business_available_seats -= 1
            else:
                flight.economy_available_seats -= 1

            self.session.commit()

            self.reservation_service.release_ticket(flight.id, seat_number)

            return ticket
        except Exception as e:
            self.session.rollback()

            self.reservation_service.release_ticket(flight.id, seat_number)

            raise e



