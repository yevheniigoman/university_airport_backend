from dependencies import get_session
from models import City, Flight, Airport
from schemas.routes import RouteRead
from services import RouteService
from sqlalchemy import select, exc
from sqlalchemy.orm import Session, joinedload, aliased
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()


@router.get("/search", tags=["routes"], response_model=list[RouteRead])
def search_routes(
    from_city: str,
    to_city: str,
    session: Session = Depends(get_session)
):
    # find <from_city>
    stmt = select(City).where(City.name == from_city).options(joinedload(City.airports))
    result = session.execute(stmt)
    try:
        dep_city = result.unique().scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail=f"City {from_city} doesn't exist")
    
    # find <to_city>
    stmt = select(City).where(City.name == to_city).options(joinedload(City.airports))
    result = session.execute(stmt)
    try:
        arr_city = result.unique().scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail=f"City {to_city} doesn't exist")

    routes_str = RouteService.search_routes(session, dep_city, arr_city)

    routes = []
    DepAirport = aliased(Airport)
    ArrAirport = aliased(Airport)
    DepCity = aliased(City)
    ArrCity = aliased(City)
    stmt = (
        select(Flight, DepAirport, ArrAirport, DepCity, ArrCity)
        .join(DepAirport, Flight.dep_airport_id == DepAirport.id)
        .join(ArrAirport, Flight.arr_airport_id == ArrAirport.id)
        .join(DepCity, DepAirport.city_id == DepCity.id)
        .join(ArrCity, ArrAirport.city_id == ArrCity.id)
    )
    for flight_numbers in routes_str:
        result = session.execute(stmt.where(Flight.flight_number.in_(flight_numbers)))
        flights = result.scalars().all()
        routes.append(RouteRead(flights=flights))

    return routes
