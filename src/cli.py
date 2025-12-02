from db import create_tables, drop_tables
import typer


cli = typer.Typer()

@cli.command()
def init_tables() -> None:
    "Creates all tables in database."
    create_tables()
    print("Done.")

@cli.command()
def remove_tables() -> None:
    "Removes all tables from database."
    drop_tables()
    print("Done.")


if __name__ == "__main__":
    cli()