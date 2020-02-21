from datetime import datetime
import json
import re
from uuid import uuid4


def installment_payments_transformer(transaction, source):
    if transaction["סוג עסקה"] == "תשלומים":
        m = re.match(r"תשלום (\d+) מתוך (\d+)", transaction["הערות"])
        if int(m[1]) == 1:
            return transaction["סכום עסקה מקורי"]
        else:
            return 0.01
    else:
        return default_transformer(transaction, source)


def amount_transformer(transaction, source):
    if transaction[source] < 0:
        return -transaction[source]
    return transaction[source]


def foreign_currency_transformer(transaction, source):
    currency_map = {"₪": "ILS", "$": "USD", "€": "EUR"}
    return currency_map[transaction[source]]


def date_transformer(transaction, source):
    date = transaction[source]
    if re.match(r"\d{2}-", date):
        return datetime.strptime(date, "%d-%m-%Y").isoformat().split("T")[0]
    else:
        return date


def credit_card_name_transformer(transaction, source):
    credit_card_no = str(int(transaction[source]))
    return f"Leumicard - {credit_card_no}"


def default_transformer(transaction, source):
    return transaction[source]


def type_transformer(transaction, source):
    amount = transaction[source]
    if amount > 0:
        return "withdrawal"
    else:
        return "deposit"


column_configs = [
    {"source": "סכום חיוב", "dest": "type", "transformer": type_transformer},
    {"source": "תאריך עסקה", "dest": "date", "transformer": date_transformer},
    {"source": "שם בית העסק", "dest": "description"},
    {
        "dest": "amount",
        "source": "סכום חיוב",
        "transformer": [installment_payments_transformer, amount_transformer],
    },
    {
        "dest": "foreign_currency_code",
        "source": "מטבע עסקה מקורי",
        "transformer": foreign_currency_transformer,
    },
    {"dest": "foreign_amount", "source": "סכום עסקה מקורי"},
    {
        "dest": "destination_name",
        "source": "4 ספרות אחרונות של כרטיס האשראי",
        "transformer": credit_card_name_transformer,
    },
]


def transform_transaction(transaction: dict):
    transformed = {}
    for conf in column_configs:
        try:
            transformers = conf.get("transformer", default_transformer)
            if not isinstance(transformers, list):
                transformers = [transformers]
            temp = transaction.copy()
            for transformer in transformers:
                temp[conf["source"]] = transformer(temp, conf["source"])
            transformed[conf["dest"]] = temp[conf["source"]]
        except:
            print(transaction)
            raise
    transformed = {
        **transformed,
        **{
            "currency_code": "ILS",
            "source_name": "Leumi",
            "notes": json.dumps(transaction, ensure_ascii=False),
            "external_id": uuid4().hex,
        },
    }
    if transformed["type"] == "deposit":
        temp = transformed["source_name"]
        transformed["source_name"] = transformed["destination_name"]
        transformed["destination_name"] = temp
    return transformed


def transform_transactions(transactions: list) -> list:
    res = []
    for transaction in transactions:
        transformed = transform_transaction(transaction)
        res.append(transformed)
        print(
            "processed: {date} - {type} - {description} - {amount}".format(
                **transformed
            )
        )
    return res
