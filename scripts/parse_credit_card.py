import datetime
import json
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.cash_flow import CashFlow
from parsers.isracard_parser import IsraCardParser

UUID_NAMESPACE = uuid.UUID("c9def9830ffd4a2293aeb804e0d121ec")


def datetime_converter(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()


def transaction_to_to_cash_model(transaction, source, extra=""):
    kwargs = {
        "date": transaction.date,
        "name": transaction.business,
        "value": transaction.value,
        "source": source,
        "id": uuid.uuid4().hex,
        "details": json.dumps(transaction.to_dict(), default=datetime_converter),
    }
    return CashFlow(**kwargs)


def parse_credit_card(type, excel_file, out=None, storage=None):
    parsers = {"leumicard": LeumiCardParser, "isracard": IsraCardParser}
    sources = {"leumicard": "Leumicard", "isracard": "Isracard"}
    res = parsers[type](excel_file).parse()
    transactions = [t.to_dict() for t in res.transactions]
    if out is not None:
        with open(out, "wb") as fp:
            json.dump(transactions, fp, default=datetime_converter)
    elif storage is not None:
        engine = create_engine(storage)
        Session = sessionmaker(bind=engine)
        session = Session()
        cf_objects = []
        for cf in res.transactions:
            cf_objects.append(transaction_to_to_cash_model(cf, sources[type]))
        try:
            session.add_all(cf_objects)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
    else:
        print(json.dumps(transactions, default=datetime_converter, indent=2))
