from auth import fastapi_auth, auth_backend
from routers import flights
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

app.include_router(flights.router)


@app.get("/")
def index():
    return {"name": "Aiport ticket database"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
