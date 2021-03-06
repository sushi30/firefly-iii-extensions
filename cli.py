import csv
import os
import click
from dotenv import load_dotenv
from tqdm import tqdm
from lib import cli_leumi
from parsers.leumicard import parse_file
from parsers.lib import add_external_ids
from rules import import_rules
from src.api_calls import (
    get_transactions,
    post_budget,
    post_category,
    post_tag,
    post_transaction,
    validate_transactions,
)
from src.transaction import Transaction
from src.transaction_configs.leumicard import transform_transactions
from src.writers import write_csv

load_dotenv()


@click.group()
def cli():
    pass


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
@click.option("--page", type=click.INT)
def delete(page):
    res = get_transactions({"page": page}).json()
    transactions = [Transaction(t["id"], **t["attributes"]) for t in res["data"]]
    for transaction in tqdm(transactions):
        if (
            transaction.attributes["transactions"][0]["destination_id"] == 3
            or transaction.attributes["transactions"][0]["source_id"] == 3
        ):
            transaction.delete()


@cli.command()
@click.argument("path", type=click.File(mode="rb"))
def leumicard(path):
    print("turning csv to records")
    transactions = parse_file(path)
    print("transform to transactions")
    transactions = transform_transactions(transactions)
    print("adding ids")
    transactions = add_external_ids(transactions, os.path.basename(path.name))
    print("validating schemas")
    validate_transactions(transactions)
    print("writing to csv")
    write_csv("tmp/leumicard.csv", sorted(transactions, key=lambda x: x["date"]))


@cli.command()
@click.argument("path", type=click.File(mode="r", encoding="utf8"))
def leumi(path):
    cli_leumi(path)


@cli.command()
@click.argument("path", type=click.File(mode="r", encoding="utf8"))
@click.option("--start", "-s", type=click.INT, default=0)
def import_csv(path, start):
    reader = csv.DictReader(path)
    rows = [r for r in reader]
    print("posting transactions")
    for row in tqdm(rows[start:]):
        print("\n{type} - {description} - {date} - {amount}".format(**row))
        post_transaction(row)


if __name__ == "__main__":
    cli()
