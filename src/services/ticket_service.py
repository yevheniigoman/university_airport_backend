from models import Ticket, Flight, Seat
from schemas.tickets import Passenger
from services import ReservationService
from sqlalchemy.orm import Session
from datetime import datetime


class TicketService:
    @staticmethod
    def buy(
        session: Session,
        passenger: Passenger,
        flight: Flight,
        seat: Seat
    ) -> Ticket:
        # check if there are available seats
        available_seats = flight.business_available_seats + flight.economy_available_seats
        if available_seats <= 0:
            raise ValueError("There are no available seats left for this flight")

        # checking if the seat has been sold
        sold_ticket = session.query(Ticket).filter_by(flight_id = flight.id, seat_id = seat.id, status=1).first()
        if sold_ticket:
            raise ValueError(f"Seat {seat.seat_number} is already sold")

        # Try to reserve seat in Redis (atomic lock)
        reserved = ReservationService.reserve_ticket(flight.id, seat.seat_number)

        if not reserved:
            raise ValueError(f"Seat {seat.seat_number} is already reserved")

        price = flight.business_price if seat.seat_class == 1 else flight.economy_price

        try:
            ticket = Ticket(
                flight_id=flight.id,
                seat_id=seat.id,
                first_name=passenger.first_name,
                last_name=passenger.last_name,
                purchase_date=datetime.now(),
                price=price,
                status=1
            )
            session.add(ticket)

            if seat.seat_class == 1:
                flight.business_available_seats -= 1
            else:
                flight.economy_available_seats -= 1
            session.commit()

            ReservationService.release_ticket(flight.id, seat.seat_number)
            return ticket
        except Exception as e:
            session.rollback()
            ReservationService.release_ticket(flight.id, seat.seat_number)
            raise e
