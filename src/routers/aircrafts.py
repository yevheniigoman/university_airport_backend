from dependencies import get_session
from models import Aircraft
from schemas.aircrafts import AircraftRead
from sqlalchemy import select
from sqlalchemy.orm import Session, exc
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix="/aircrafts")


@router.get("/", tags=["aircrafts"], response_model=list[AircraftRead])
def read_aircrafts(session: Session = Depends(get_session)):
    stmt = select(Aircraft)
    result = session.execute(stmt)
    return result.scalars().all()


@router.get("/{tail_number}", tags=["aircrafts"], response_model=AircraftRead)
def read_aircraft(tail_number: str, session: Session = Depends(get_session)):
    stmt = select(Aircraft).where(Aircraft.tail_number == tail_number)
    result = session.execute(stmt)
    try:
        aircraft = result.scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return aircraft
