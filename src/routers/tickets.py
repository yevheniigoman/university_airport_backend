from dependencies import get_session
from models import Flight, Seat, Ticket
from schemas.tickets import TicketCreate, Passenger
from services import TicketService, TicketReportService
from sqlalchemy import select, exc
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Response


router = APIRouter(prefix="/tickets")


@router.post("/", tags=["tickets"])
def create_ticket(
    ticket_data: TicketCreate,
    session: Session = Depends(get_session)
):
    # find flight
    stmt = select(Flight).where(Flight.flight_number == ticket_data.flight_number)
    result = session.execute(stmt)
    try:
        flight = result.scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # find seat
    stmt = (
        select(Seat)
        .where(Seat.aircraft_id == flight.aircraft_id)
        .where(Seat.seat_number == ticket_data.seat_number)
    )
    result = session.execute(stmt)
    try:
        seat = result.scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Seat not found")
    
    passanger = Passenger(ticket_data.first_name, ticket_data.last_name)

    try:
        ticket = TicketService.buy(session, passanger, flight, seat)
    except:
        raise HTTPException(status_code=500)
    
    stmt = (
        select(Ticket)
        .join(Flight, Ticket.flight_id == Flight.id)
        .join(Seat, Ticket.seat_id == Seat.id)
        .where(Ticket.id == ticket.id)
    )
    result = session.execute(stmt)
    ticket = result.scalars().one()
    pdf = TicketReportService.to_pdf(ticket)

    filename = f"ticket_{ticket.id}.pdf"
    headers = {
        f"Content-Disposition": f"attachment; filename={filename}"
    }
    return Response(
        bytes(pdf.output()),
        media_type="application/pdf",
        headers=headers
    )
