from parsers.isracard_parser import IsraCardParser
from scripts.parse_credit_card import datetime_converter


def test_parse_isracard():
    with open("tests/data/isracard_test_data.xls", "rb") as excel_file:
        icp = IsraCardParser(excel_file).parse()
    assert len(icp.transactions) == 14
    print(icp.dumps(default=datetime_converter, indent=2))
