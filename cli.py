import json
import os

import click
from dotenv import load_dotenv
from tqdm import tqdm
import typing

from parsers.excel_to_records import leumicard_excel_to_records
from parsers.post_transactions import post_transaction
from parsers.transform_transactions import transform_transactions

load_dotenv()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("path", type=click.File(mode="rb"))
def leumicard(path):
    file_name = os.path.basename(path.name)
    transactions = leumicard_excel_to_records(path)
    transactions = transform_transactions(transactions)
    transactions =
    # for transaction in tqdm(transactions[:2]):
    #     post_transaction(transaction)


if __name__ == "__main__":
    cli()
