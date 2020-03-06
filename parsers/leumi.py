from datetime import datetime, timedelta
import json
from lxml import html


def parse_html(file):
    root = html.fromstring(file.read())
    headers = root.xpath(
        "//table[@id='WorkSpaceBox']//tr[@class='header']//th[not(contains(@class,'Hidden'))]"
    )[1:]
    categories = [h.text_content().strip() for h in headers]
    rows = root.xpath("//table[@id='WorkSpaceBox']//tr[contains(@class, 'Item')]")
    rows = [[c.text_content().strip() for c in row.getchildren()][1:7] for row in rows]
    rows = [dict(zip(categories, row)) for row in rows]
    return rows


def parse_transaction(transaction: dict):
    res = {}
    if type(transaction["תאריך"]) == str:
        res["date"] = datetime.strptime(transaction["תאריך"], "%d/%m/%y")
    else:
        date = datetime(1900, 1, 1) + timedelta(days=transaction["תאריך"] - 2)
        res["date"] = datetime(date.year, date.day, date.month)
    res["date"] = res["date"].isoformat().split("T")[0]
    if len(str(transaction["חובה"])) > len(str(transaction["זכות"])):
        res["type"] = "withdrawal"
        res["amount"] = float(transaction["חובה"].replace(",", ""))
    else:
        res["type"] = "deposit"
        res["amount"] = float(transaction["זכות"].replace(",", ""))
    res["description"] = transaction["תיאור"]
    res["notes"] = json.dumps(transaction, ensure_ascii=False)
    return res


def filter_transactions(transactions):
    res = []
    for transaction in transactions:
        if "לאומי ויזה" in transaction["description"]:
            continue
        else:
            res.append(transaction)
    return res
