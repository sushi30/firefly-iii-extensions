import json

from dotenv import load_dotenv
from parsers.post_transactions import post

load_dotenv()


def test_leumicard_post_transactions():
    with open(
        "tests/data/leumicard_test_parsed_transactions.json", "r", encoding="utf8"
    ) as fp:
        transactions = json.load(fp)
    res = post(transactions)
    print(res)


def test_post_revenue():
    res = post(
        [
            {
                "type": "deposit",
                "date": "2019-01-06",
                "description": "העברה באפליקציית PAYBOX",
                "amount": 100.0,
                "foreign_currency_code": "ILS",
                "foreign_amount": 100.0,
                "destination_name": "Leumi 3582271",
                "currency_code": "ILS",
                "source_name": "Leumicard - 1234",
                "notes": '{"תאריך עסקה": "2019-01-06", "שם בית העסק": "העברה באפליקציית PAYBOX", "קטגוריה": "שונות", "4 ספרות אחרונות של כרטיס האשראי": 1234.0, "סוג עסקה": "רגילה", "סכום חיוב": -100.0, "מטבע חיוב": "₪", "סכום עסקה מקורי": 100.0, "מטבע עסקה מקורי": "₪", "תאריך חיוב": "2019-02-03", "הערות": "", "מועדון הנחות": "", "מפתח דיסקונט": "", "אופן ביצוע ההעסקה": "טלפוני", "שער המרה ממטבע מקור/התחשבנות לש\\"ח": ""}',
                "external_id": "767eb0a9d6824d3d95bc20f09628907c",
            }
        ]
    )
    print(res)


def test_post_expense():
    res = post(
        [
            {
                "date": "2019-10-07",
                "description": "איקאה-ריהוט ועיצוב הבית",
                "amount": 1528.0,
                "foreign_currency_code": "ILS",
                "foreign_amount": 1528.0,
                "destination_name": "Leumicard - 4941",
                "type": "withdrawal",
                "currency_code": "ILS",
                "source_name": "Leumi 3582271",
                "notes": '{"תאריך עסקה": "07-10-2019", "שם בית העסק": "איקאה-ריהוט ועיצוב הבית", "קטגוריה": "מוצרי חשמל", "4 ספרות אחרונות של כרטיס האשראי": "4941", "סוג עסקה": "תשלומים", "סכום חיוב": 510.0, "מטבע חיוב": "₪", "סכום עסקה מקורי": 1528.0, "מטבע עסקה מקורי": "₪", "תאריך חיוב": "03-11-2019", "הערות": "תשלום 1 מתוך 3", "מועדון הנחות": "", "מפתח דיסקונט": "", "אופן ביצוע ההעסקה": "בנוכחות כרטיס", "שער המרה ממטבע מקור/התחשבנות לש\\"ח": ""}',
                "external_id": "b693e0652ae64350af8bd433b257336a",
            }
        ]
    )
    print(res)
