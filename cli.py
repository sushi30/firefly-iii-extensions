import click
from dotenv import load_dotenv
from tqdm import tqdm

from parsers.excel_to_records import leumicard_excel_to_records
from parsers.post_transactions import post_transaction
from parsers.transform_transactions import transform_transactions
from scripts.create_tables import create_tables

load_dotenv()


@click.group()
def cli():
    pass


def decorate(f):
    for dec in [
        click.argument("path", type=click.File(mode="rb")),
        click.option("--out", default=None),
        click.option("--storage", default=None),
        cli.command(),
    ]:
        f = dec(f)
    return f


@cli.group()
def categorize():
    pass


@categorize.command()
@click.argument("storage")
def names(storage):
    categorize_by_name(storage)


@decorate
def isracard(out, storage, path):
    inner("isracard", path, out, storage)


@cli.command()
@click.argument("path", type=click.File(mode="rb"))
def leumicard(path):
    transactions = leumicard_excel_to_records(path)
    transactions = transform_transactions(transactions)
    # for transaction in tqdm(transactions):
    #     post_transaction(transaction)


@cli.command()
@click.argument("storage")
def tables(storage):
    create_tables(storage)


if __name__ == "__main__":
    cli()
