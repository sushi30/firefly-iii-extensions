import os
from dotenv import load_dotenv
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()


def test_join():
    engine = create_engine("mysql://root:1234@localhost:3306/finance")
    Session = sessionmaker(bind=engine)
    session = Session()
    print(
        session.query(CashFlow)
        .outerjoin(GeneralCashFlowMapping, CashFlow.name == GeneralCashFlowMapping.name)
        .all()
    )


def test_firefly_api():
    res = requests.get(
        os.environ["ENDPOINT"] + "/api/v1/about",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["TOKEN"],
        },
    )
    assert "login" not in res.url
