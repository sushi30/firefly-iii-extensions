from uuid import uuid5, UUID

NAMESPACE = UUID("5f7303db-7348-410e-bb15-6b9932e524a9")


def add_external_ids(transactions: list, file_name: str) -> list:
    return [
        {**t, "external_id": uuid5(NAMESPACE, file_name + str(i)).hex}
        for i, t in enumerate(transactions)
    ]
