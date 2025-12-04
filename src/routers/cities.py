from dependencies import get_session
from models import City
from schemas.cities import CityRead
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends


router = APIRouter(prefix="/cities", tags=["cities"])


@router.get("/", response_model=list[CityRead])
def read_cities(session: Session = Depends(get_session)):
    stmt = select(City)
    result = session.execute(stmt)
    return result.scalars().all()
