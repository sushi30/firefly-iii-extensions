import os
from dotenv import load_dotenv
import requests

load_dotenv()


def test_firefly_api():
    res = requests.get(
        os.environ["ENDPOINT"] + "/api/v1/about",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["TOKEN"],
        },
    )
    res.raise_for_status()
    assert "login" not in res.url


def test_firefly_user():
    res = requests.get(
        os.environ["ENDPOINT"] + "/api/v1/about/user",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["TOKEN"],
        },
    )
    res.raise_for_status()
    print(res.content)
    assert "login" not in res.url
