def create_tables() -> None:
    import models
    from db import engine, Base

    Base.metadata.create_all(engine)

def drop_tables() -> None:
    import models
    from db import engine, Base

    Base.metadata.drop_all(engine)

def import_csv(table: str, filepath: str, if_exists: str = "append") -> None:
    import pandas as pd
    from db import engine

    df = pd.read_csv(filepath)
    
    with engine.connect() as conn:
        df.to_sql(table, conn, if_exists=if_exists, index=False)