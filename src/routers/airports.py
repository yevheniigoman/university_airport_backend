from dependencies import get_session
from models import Airport
from schemas.airports import AirportRead
from sqlalchemy import select, exc
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(prefix="/airports")


@router.get("/{airport_code}", tags=["airports"], response_model=AirportRead)
def read_airport(
    airport_code: str,
    session: Session = Depends(get_session)
):
    stmt = select(Airport).where(Airport.code == airport_code)
    result = session.execute(stmt)
    try:
        airport = result.scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Airport not found")
    return airport
