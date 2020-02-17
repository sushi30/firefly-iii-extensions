import json
from parsers.transform_transactions import transform_transactions, transform_transaction


def test_leumicard_transaction_transformers():
    with open("tests/data/leumicard_test_data.json", "r", encoding="utf8") as fp:
        transactions = json.load(fp)
    transformed = transform_transactions(transactions)
    print("\n", json.dumps(transformed, ensure_ascii=False, indent=2))


def test_transform_expense():
    res = transform_transaction(
        {
            "תאריך עסקה": "2019-01-03",
            "שם בית העסק": "ניצת הדובדבן טבריה",
            "קטגוריה": "מזון וצריכה",
            "4 ספרות אחרונות של כרטיס האשראי": 1234.0,
            "סוג עסקה": "רגילה",
            "סכום חיוב": 30.0,
            "מטבע חיוב": "₪",
            "סכום עסקה מקורי": 30.0,
            "מטבע עסקה מקורי": "₪",
            "תאריך חיוב": "2019-02-03",
            "הערות": "",
            "מועדון הנחות": "",
            "מפתח דיסקונט": "",
            "אופן ביצוע ההעסקה": "בנוכחות כרטיס",
            'שער המרה ממטבע מקור/התחשבנות לש"ח': "",
        }
    )
    print("\n", json.dumps(res, ensure_ascii=False, indent=2))
    assert res["type"] == "withdrawal"
    assert res["destination_name"] == "Leumicard - 1234"
    assert res["source_name"] == "Leumi 3582271"


def test_transform_revenue():
    res = transform_transaction(
        {
            "תאריך עסקה": "2019-01-06",
            "שם בית העסק": "העברה באפליקציית PAYBOX",
            "קטגוריה": "שונות",
            "4 ספרות אחרונות של כרטיס האשראי": 1234.0,
            "סוג עסקה": "רגילה",
            "סכום חיוב": -100.0,
            "מטבע חיוב": "₪",
            "סכום עסקה מקורי": 100.0,
            "מטבע עסקה מקורי": "₪",
            "תאריך חיוב": "2019-02-03",
            "הערות": "",
            "מועדון הנחות": "",
            "מפתח דיסקונט": "",
            "אופן ביצוע ההעסקה": "טלפוני",
            'שער המרה ממטבע מקור/התחשבנות לש"ח': "",
        }
    )
    print("\n", json.dumps(res, ensure_ascii=False, indent=2))
    assert res["type"] == "deposit"
    assert res["source_name"] == "Leumicard - 1234"
    assert res["destination_name"] == "Leumi 3582271"


def test_payment_installment():
    res = transform_transaction(
        {
            "תאריך עסקה": "22-11-2019",
            "שם בית העסק": "נעלי ניוז",
            "קטגוריה": "הלבשה והנעלה",
            "4 ספרות אחרונות של כרטיס האשראי": "3547",
            "סוג עסקה": "תשלומים",
            "סכום חיוב": 70.0,
            "מטבע חיוב": "₪",
            "סכום עסקה מקורי": 700.0,
            "מטבע עסקה מקורי": "₪",
            "תאריך חיוב": "02-02-2020",
            "הערות": "תשלום 3 מתוך 10",
            "מועדון הנחות": "",
            "מפתח דיסקונט": "",
            "אופן ביצוע ההעסקה": "בנוכחות כרטיס",
            'שער המרה ממטבע מקור/התחשבנות לש"ח': "",
        }
    )
    print("\n", json.dumps(res, ensure_ascii=False, indent=2))
    assert res["amount"] == 0.01
