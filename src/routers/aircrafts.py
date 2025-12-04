from dependencies import get_session
from models import Aircraft
from schemas.aircrafts import AircraftRead
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/aircrafts")


@router.get("/", tags=["aircrafts"], response_model=list[AircraftRead])
def read_aircrafts(session: Session = Depends(get_session)):
    stmt = select(Aircraft)
    result = session.execute(stmt)
    return result.scalars().all()
