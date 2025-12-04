from db import utils
import typer


cli = typer.Typer()

@cli.command()
def create_tables() -> None:
    "Creates all tables in database."
    utils.create_tables()
    print("Done.")

@cli.command()
def drop_tables() -> None:
    "Drops all tables from database."
    utils.drop_tables()
    print("Done.")

@cli.command()
def import_csv(table: str, filepath: str) -> None:
    """
    Imports data from csv file into table.
    If table already contains data, new data from <filepath> file
    will be appended into table.
    """
    try:
        utils.import_csv(table, filepath)
    except FileNotFoundError:
        print("Error: File doesn't exists.")
        return

    print("Done.")


if __name__ == "__main__":
    cli()