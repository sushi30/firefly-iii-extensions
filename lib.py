import os
from parsers.leumi import parse_excel, parse_transaction
from parsers.lib import add_external_ids, transaction_defaults
from src.api_calls import validate_transactions, post_transaction


def cli_leumi(file):
    print("turning excel to records")
    transactions = parse_excel(file)
    print("parsing transactions")
    transformed = []
    for transaction in transactions:
        transaction_t = parse_transaction(transaction)
        print("{type} - {date} - {description} - {amount}".format(**transaction_t))
        transformed.append(transaction_t)
    transformed = [transaction_defaults(t) for t in transformed]
    print("adding ids")
    transactions = add_external_ids(transformed, os.path.basename(file.name))
    print("validating schemas")
    validate_transactions(transactions)
    # print("posting to firefly iii")
    # for transaction in tqdm(transactions):
    #     post_transaction(transaction)
