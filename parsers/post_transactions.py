import os

import requests


def post_transaction(transaction):
    res = requests.post(
        os.environ["ENDPOINT"] + "/api/v1/transactions",
        json={"transactions": [transaction]},
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["TOKEN"],
        },
    )
    res.raise_for_status()
    if "login" in res.url:
        raise Exception("Firefly III Login")
    return res


def post_transactions(transactions):
    res = []
    for transaction in transactions:
        try:
            res.append(post_transaction(transaction))
        except:
            print(transaction)
            raise
    return res
