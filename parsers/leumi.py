from datetime import datetime, timedelta
import json
import xlrd
from .lib import parse_rows


def parse_excel(file):
    rows = []
    wb = xlrd.open_workbook(file_contents=file.read())
    for i in range(wb.nsheets):
        it = iter(wb.sheet_by_index(i).get_rows())
        while True:
            try:
                row = next(it)
            except StopIteration:
                break
            if type(row[0].value) == str and "תנועות בחשבון" == row[0].value:
                for _ in range(4):
                    row = next(it)
                categories = [col.value for col in row]
                parse_rows(rows, it, categories)
    return rows


def parse_transaction(transaction: dict):
    res = {}
    if type(transaction["תאריך"]) == str:
        res["date"] = datetime.strptime(transaction["תאריך"], "%d/%m/%y")
    else:
        res["date"] = datetime(1900, 1, 1) + timedelta(days=transaction["תאריך"] - 2)
    res["date"] = res["date"].isoformat().split("T")[0]
    if len(str(transaction["חובה"])) > len(str(transaction["זכות"])):
        res["type"] = "withdrawal"
        res["amount"] = float(transaction["חובה"])
    else:
        res["type"] = "deposit"
        res["amount"] = float(transaction["זכות"])
    res["description"] = transaction["תיאור"]
    res["notes"] = json.dumps(transaction, ensure_ascii=False)
    return res
