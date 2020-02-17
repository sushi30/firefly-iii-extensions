from sqlalchemy import create_engine
from app.models.cash_flow import CashFlow
from app.models.cash_flow_mapping import SpecificCashFlowMapping, GeneralCashFlowMapping


def create_tables(storage):
    engine = create_engine(storage)
    CashFlow.metadata.create_all(engine)
    SpecificCashFlowMapping.metadata.create_all(engine)
    GeneralCashFlowMapping.metadata.create_all(engine)


