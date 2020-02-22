import json
import os
import click
from dotenv import load_dotenv
from tqdm import tqdm

from rules import import_rules
from src.api_calls import post_budget, post_tag, post_category, get_transactions
from src.excel_to_records import leumicard_excel_to_records
from src.external_ids import add_external_ids
from src.api_calls import post_transaction, validate_transactions
from src.transaction import Transaction
from src.transform_transactions import transform_transactions

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


@cli.command()
@click.argument("budget_name")
def budget(budget_name):
    post_budget(budget_name)
    post_tag(budget_name)
    post_category(budget_name)


@cli.group()
def transactions():
    pass


@cli.group()
def rules():
    pass


@rules.command("import")
@click.argument("path", type=click.File(mode="r", encoding="utf8"))
def _import(path):
    import_rules(path)


@transactions.command()
@click.argument("parameters", required=False)
def delete(parameters):
    parameters = json.loads(parameters or "{}")
    res = get_transactions(parameters).json()
    transactions = [Transaction(t["id"], **t["attributes"]) for t in res["data"]]
    for transaction in tqdm(transactions):
        transaction.delete()


@cli.command()
@click.argument("path", type=click.File(mode="rb"))
def leumicard(path):
    print("turning csv to records")
    transactions = leumicard_excel_to_records(path)
    print("transform to transactions")
    transactions = transform_transactions(transactions)
    print("adding ids")
    transactions = add_external_ids(transactions, os.path.basename(path.name))
    print("validating schemas")
    validate_transactions(transactions)
    print("posting to firefly iii")
    for transaction in tqdm(transactions):
        post_transaction(transaction)


if __name__ == "__main__":
    cli()
