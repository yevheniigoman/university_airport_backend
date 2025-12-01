def create_tables() -> None:
    import models
    from db import engine, Base

    Base.metadata.create_all(engine)
