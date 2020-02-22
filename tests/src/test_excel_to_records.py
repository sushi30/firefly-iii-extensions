from src.excel_to_records import leumi_to_records


def test_leumi_to_records():
    with open("tests/data/leumi_data.xls", mode="rb") as fp:
        res = leumi_to_records(fp)
    print(res)
