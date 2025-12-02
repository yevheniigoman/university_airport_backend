def create_tables() -> None:
    import models
    from db import engine, Base

    Base.metadata.create_all(engine)

def drop_tables() -> None:
    import models
    from db import engine, Base

    Base.metadata.drop_all(engine)