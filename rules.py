import csv
import os

import requests

from src.api_calls import response_wrapper


def import_rules(path):
    reader = csv.DictReader(path)
    rows = [row for row in reader]
    rules = [dict(row) for row in rows if row["row_contains"] == "rule"]
    for rule in rules:
        rule_id = rule["rule_id"]
        rule["triggers"] = [
            row
            for row in rows
            if row["row_contains"] == "trigger" and row["rule_id"] == rule_id
        ]
        rule["actions"] = [
            row
            for row in rows
            if row["row_contains"] == "action" and row["rule_id"] == rule_id
        ]
    for rule in rules:
        for key in [
            "user_id",
            "rule_id",
            "row_contains",
            "created_at",
            "updated_at",
            "order",
            "group_name",
            "description",
            *[
                k
                for k in rule.keys()
                if any(keyword in k for keyword in ["trigger_", "action_"])
            ],
        ]:
            del rule[key]
        rule["strict"] = False
        rule["active"] = True
        rule["stop_processing"] = False
        rule["triggers"] = [
            {k.replace("trigger_", ""): v for k, v in t.items() if "trigger_" in k}
            for t in rule["triggers"]
        ]
        rule["actions"] = [
            {k.replace("action_", ""): v for k, v in t.items() if "action_" in k}
            for t in rule["actions"]
        ]
        for trigger in rule["triggers"]:
            trigger["stop_processing"] = False
            trigger["active"] = True
            del trigger["order"]
        for trigger in rule["actions"]:
            trigger["stop_processing"] = False
            trigger["active"] = True
            del trigger["order"]
    print(rules)


def post_rule(rule):
    return response_wrapper(
        requests.post(
            os.environ["ENDPOINT"] + "/api/v1/rules",
            json=rule,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + os.environ["TOKEN"],
            },
        )
    )
