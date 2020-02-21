import os
import yaml
import requests
from jsonschema import validate

with open("schemas/TransactionSplit.yaml") as fp:
    transaction_schema = yaml.load(fp, Loader=yaml.FullLoader)


def validate_transactions(transactions: list):
    for transaction in transactions:
        validate(transaction, transaction_schema["TransactionSplit"])


def post_wrapper(*args, **kwargs):
    res = requests.post(*args, **kwargs)
    res.raise_for_status()
    if "login" in res.url:
        raise Exception("Firefly III Login")
    return res


def post_transaction(transaction):
    return post_wrapper(
        os.environ["ENDPOINT"] + "/api/v1/transactions",
        json={"transactions": [transaction]},
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["TOKEN"],
        },
    )


def post_transactions(transactions):
    res = []
    for transaction in transactions:
        try:
            res.append(post_transaction(transaction))
        except:
            print(transaction)
            raise
    return res


def post_budget(budget):
    return post_wrapper(
        os.environ["ENDPOINT"] + "/api/v1/budgets",
        json={"name": budget},
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["TOKEN"],
        },
    )


def post_tag(tag):
    return post_wrapper(
        os.environ["ENDPOINT"] + "/api/v1/tags",
        json={"tag": tag},
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["TOKEN"],
        },
    )


def post_category(category):
    return post_wrapper(
        os.environ["ENDPOINT"] + "/api/v1/categories",
        json={"name": category},
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["TOKEN"],
        },
    )
