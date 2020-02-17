from datetime import datetime
import jwt
import pytest
from jwt import ExpiredSignatureError
from auth import PRIVATE_KEY
from auth.authorize import auth


@pytest.fixture
def token():
    return jwt.encode(
        {
            "sub": "demo",
            "iat": datetime.fromisoformat("2019-10-22T10:00"),
            "exp": datetime.fromisoformat("2019-10-22T16:00"),
        },
        PRIVATE_KEY,
        algorithm="HS256",
    )


@pytest.mark.freeze_time("2019-10-20 00:00")
def test_authorize(token):
    user = auth(token)
    assert user == "demo"


@pytest.mark.freeze_time("2019-10-24")
def test_expired(token):
    with pytest.raises(ExpiredSignatureError):
        auth(token)
