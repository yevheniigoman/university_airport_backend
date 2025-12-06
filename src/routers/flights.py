from dependencies import get_session
from auth import get_current_active_user
from models import Flight, Aircraft, Airport
from schemas.flights import FlightRead, FlightCreate
from services import FlightService, FlightReportService
from sqlalchemy import select, exc
from sqlalchemy.orm import Session, aliased
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from services.route_service import RouteService


router = APIRouter(prefix="/flights")
route_service = RouteService()

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

    # Neo4j sync
    try:
        route_service.sync_flight_created(flight)
    except Exception as e:
        return JSONResponse(
            {"success": False, "errors": [f"Neo4j sync failed: {str(e)}"]},
            status_code=500
        )


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



@router.delete("/{flight_number}", tags=["flights"])
def delete_flight(
    flight_number: str,
    session: Session = Depends(get_session)
):

    flight = session.query(Flight).filter_by(flight_number=flight_number).first()

    if not flight:
        return JSONResponse(
            {"success": False, "errors": [f"Flight '{flight_number}' not found"]},
            status_code=404
        )

    # Save codes before delete
    dep_code = flight.dep_airport.code
    arr_code = flight.arr_airport.code

    # Delete Neo4j edge first
    try:
        route_service.delete_flight_edge(
            dep_code=dep_code,
            arr_code=arr_code,
            flight_number=flight_number
        )
    except Exception as e:
        return JSONResponse(
            {"success": False, "errors": [f"Neo4j sync failed: {str(e)}"]},
            status_code=500
        )

    # Delete from MySQL
    try:
        session.delete(flight)
        session.commit()
    except Exception as e:
        session.rollback()
        return JSONResponse({"success": False, "errors": [str(e)]}, status_code=422)

    return JSONResponse({"success": True, "errors": []}, status_code=200)
