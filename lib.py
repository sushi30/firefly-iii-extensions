import os
from parsers.leumi import filter_transactions, parse_html, parse_transaction
from parsers.lib import add_external_ids, transaction_defaults
from src.api_calls import validate_transactions
from src.writers import write_csv


def cli_leumi(file):
    print("turning excel to records")
    transactions = parse_html(file)
    print("parsing transactions")
    transformed = []
    for transaction in transactions:
        transaction_t = parse_transaction(transaction)
        transformed.append(transaction_t)
    transformed = filter_transactions(transformed)
    for transaction in transformed:
        print("{type} - {date} - {description} - {amount}".format(**transaction))
    transformed = [transaction_defaults(t) for t in transformed]
    print("adding ids")
    transactions = add_external_ids(transformed, os.path.basename(file.name))
    print("validating schemas")
    validate_transactions(transactions)
    print("writing to csv")
    write_csv("tmp/leumi.csv", transactions)
