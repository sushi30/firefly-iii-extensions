import json
from parsers.excel_to_records import leumicard_excel_to_records
from scripts.parse_credit_card import datetime_converter


def test_parse_leumicard():
    with open("tests/data/leumicard_test_data.xlsx", "rb") as file:
        res = leumicard_excel_to_records(file)
    assert len(res) == 22
    print(
        "\n", json.dumps(res, default=datetime_converter, indent=2, ensure_ascii=False)
    )
