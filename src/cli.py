from db import create_tables
import typer


cli = typer.Typer()

@cli.command()
def init_tables() -> None:
    "Creates all tables in database."
    create_tables()
    print("Done.")


if __name__ == "__main__":
    cli()