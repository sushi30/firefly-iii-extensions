from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.cash_flow import CashFlow
from app.models.cash_flow_mapping import GeneralCashFlowMapping


def test_join():
    engine = create_engine("mysql://root:1234@localhost:3306/finance")
    Session = sessionmaker(bind=engine)
    session = Session()
    print(session.query(CashFlow).outerjoin(GeneralCashFlowMapping, CashFlow.name == GeneralCashFlowMapping.name).all())
