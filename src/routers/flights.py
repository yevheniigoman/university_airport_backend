from dependencies import get_session
from auth import get_current_active_user
from models import Flight, Aircraft, Airport
from schemas.flights import FlightRead, FlightCreate
from services import FlightService, FlightReportService
from sqlalchemy import select, exc
from sqlalchemy.orm import Session, aliased
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/flights")


@router.get("/{flight_number}", tags=["flights"], response_model=FlightRead)
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


@router.post("/", tags=["flights"], dependencies=[Depends(get_current_active_user)])
def create_flight(
    flight_data: FlightCreate,
    session: Session = Depends(get_session)
):
    try:
        flight = FlightService.create_flight(session, flight_data)
    except Exception as e:
        return JSONResponse(
            {"success": False, "errors": [str(e)]},
            status_code=422
        )

    session.add(flight)
    session.commit()
    return JSONResponse({"success": True, "errors": []}, status_code=200)


@router.get("/{flight_number}/report", tags=["reports"], dependencies=[Depends(get_current_active_user)])
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
