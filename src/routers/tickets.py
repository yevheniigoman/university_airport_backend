from dependencies import get_session
from models import Flight
from schemas.tickets import TicketRead
from sqlalchemy import select, exc
from sqlalchemy.orm import Session, joinedload
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()

@router.get("/flights/{flight_number}/tickets", tags=["tickets"], response_model=list[TicketRead])
def read_flight_tickets(
    flight_number: str,
    session: Session = Depends(get_session)
):
    """Returns tickets for specified flight."""
    stmt = (
        select(Flight)
        .options(joinedload(Flight.tickets))
        .where(Flight.flight_number == flight_number)
    )
    result = session.execute(stmt)
    try:
        flight = result.unique().scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Flight not found")

    return flight.tickets
