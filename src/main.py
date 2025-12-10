from auth import fastapi_auth, auth_backend
import routers
from schemas.auth import UserRead, UserCreate
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


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
app.include_router(routers.routes.router)


@app.get("/")
def index():
    return {"name": "Aiport ticket database"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
