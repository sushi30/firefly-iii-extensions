from app.models import CashFlow


def test_max():
    CashFlow.max(CashFlow.date)
