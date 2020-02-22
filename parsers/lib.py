from uuid import UUID, uuid5

NAMESPACE = UUID("5f7303db-7348-410e-bb15-6b9932e524a9")


def parse_rows(rows, it, categories):
    while True:
        try:
            row = next(it)
        except StopIteration:
            break
        rows.append({col_name: col.value for (col_name, col) in zip(categories, row)})


def transaction_defaults(transaction):
    asset_accout = "Leumi"
    res = {**transaction, **{"currency_code": "ILS"}}
    if res["type"] == "withdrawal":
        res["source_name"] = asset_accout
    else:
        res["destination_name"] = asset_accout
    return res


def add_external_ids(transactions: list, file_name: str) -> list:
    return [
        {**t, "external_id": uuid5(NAMESPACE, file_name + str(i)).hex}
        for i, t in enumerate(transactions)
    ]
