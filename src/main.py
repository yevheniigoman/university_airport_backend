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


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
