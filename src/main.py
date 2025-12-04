from auth import fastapi_auth, auth_backend
import routers
from schemas.auth import UserRead, UserCreate
import uvicorn
from fastapi import FastAPI


app = FastAPI()


app.include_router(
    fastapi_auth.get_register_router(UserRead, UserCreate),
    tags=["auth"]
)

app.include_router(
    fastapi_auth.get_auth_router(auth_backend),
    tags=["auth"]
)

app.include_router(routers.flights.router)
app.include_router(routers.tickets.router)
app.include_router(routers.airports.router)
app.include_router(routers.cities.router)
app.include_router(routers.aircrafts.router)


@app.get("/")
def index():
    return {"name": "Aiport ticket database"}


from dependencies import get_session
from services import TicketReportService
from models import Ticket, Flight, Seat
from sqlalchemy import select
from sqlalchemy.orm import Session, exc
from fastapi import Depends, HTTPException, Response
@app.get("/tickets/{ticket_id}/buy")
def buy_ticket(ticket_id: int, session: Session = Depends(get_session)):
    stmt = (
        select(Ticket)
        .join(Flight, Ticket.flight_id == Flight.id)
        .join(Seat, Ticket.seat_id == Seat.id)
        .where(Ticket.id == ticket_id)
    )
    result = session.execute(stmt)
    try:
        ticket = result.scalars().one()
    except exc.NoResultFound:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    pdf = TicketReportService.to_pdf(ticket)

    filename = f"ticket_{ticket_id}.pdf"
    headers = {
        f"Content-Disposition": f"attachment; filename={filename}"
    }
    return Response(
        bytes(pdf.output()),
        media_type="application/pdf",
        headers=headers
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
