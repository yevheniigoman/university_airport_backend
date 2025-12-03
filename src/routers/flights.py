from dependencies import get_session
from models import Flight, Aircraft, Airport
from schemas.flights import FlightRead
from services import FlightReportService
from sqlalchemy import select, exc
from sqlalchemy.orm import Session, aliased
from fastapi import APIRouter, Depends, HTTPException, Response


router = APIRouter(prefix="/flights", tags=["flights"])


@router.get("/{flight_number}", response_model=FlightRead)
def read_flight(
    flight_number: str,
    session: Session = Depends(get_session)
):
    DepAirport = aliased(Airport, name="dep_airport")
    ArrAirport = aliased(Airport, name="arr_airport")
    stmt = (
        select(
            Flight, Aircraft, DepAirport, ArrAirport
        )
        .join(Aircraft, Flight.aircraft_id == Aircraft.id)
        .join(DepAirport, Flight.dep_airport_id == DepAirport.id)
        .join(ArrAirport, Flight.arr_airport_id == ArrAirport.id)
        .where(Flight.flight_number == flight_number)
    )
    result = session.execute(stmt)
    try:
        flight = result.scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Flight not found")
    return flight


@router.get("/{flight_number}/report")
def generate_flight_report(
    flight_number: str,
    session: Session = Depends(get_session),
):
    """Generates flight report in pdf format"""
    # find requested flight
    DepAirport = aliased(Airport, name="dep_airport")
    ArrAirport = aliased(Airport, name="arr_airport")

    stmt = (
        select(
            Flight, Aircraft, DepAirport, ArrAirport
        )
        .join(Aircraft, Flight.aircraft_id == Aircraft.id)
        .join(DepAirport, Flight.dep_airport_id == DepAirport.id)
        .join(ArrAirport, Flight.arr_airport_id == ArrAirport.id)
        .where(Flight.flight_number == flight_number)
    )
    result = session.execute(stmt)
    try:
        flight = result.scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Flight not found")

    # generate pdf report
    pdf = FlightReportService.to_pdf(flight)

    filename = f"flight_{flight_number}_report.pdf"
    headers = {
        f"Content-Disposition": f"attachment; filename={filename}"
    }
    return Response(
        bytes(pdf.output()),
        media_type="application/pdf",
        headers=headers
    )
