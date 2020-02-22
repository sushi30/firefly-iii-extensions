from typing import List, Dict


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


column_configs: List[Dict] = [
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
