import csv
import requests
import os

ENDPOINT = os.environ["ENDPOINT"]

requests.post(
    ENDPOINT + "/api/v1/rules",
    json={
        "title": "First rule title.",
        "rule_group_id": 81,
        "trigger": "store-journal",
        "triggers": [
            {
                "type": "user_action",
                "value": "tag1",
                "active": True,
                "stop_processing": False,
            },
            {
                "type": "user_action",
                "value": "tag1",
                "active": True,
                "stop_processing": False,
            },
        ],
        "actions": [
            {
                "type": "set_category",
                "value": "Daily groceries",
                "order": 5,
                "active": True,
                "stop_processing": False,
            },
            {
                "type": "set_category",
                "value": "Daily groceries",
                "order": 5,
                "active": True,
                "stop_processing": False,
            },
        ],
        "description": "First rule description",
        "rule_group_title": "New rule group",
        "active": True,
        "strict": True,
        "stop_processing": False,
    },
)
