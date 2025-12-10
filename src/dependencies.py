from db import SessionLocal


def get_session():
    with SessionLocal() as session:
        yield session