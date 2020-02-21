import csv
import os
import jsonschema
import requests
from tqdm import tqdm
import yaml
from src.api_calls import response_wrapper

schema: dict = {}
for yaml_file in [
    "schemas/Rule.yaml",
    "schemas/RuleAction.yaml",
    "schemas/RuleTrigger.yaml",
]:
    with open(yaml_file) as fp:
        schema = {**schema, **yaml.load(fp, Loader=yaml.FullLoader)}
    with open("tmp/schema.yaml", "w") as fp:
        yaml.dump(schema, fp)


def parse_rules(path):
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
        rule["strict"] = False
        rule["active"] = True
        rule["rule_group_id"] = int(rule["group_id"])
        rule["stop_processing"] = False
        rule["trigger"] = "store-journal"
        for key in [
            "user_id",
            "rule_id",
            "row_contains",
            "created_at",
            "updated_at",
            "order",
            "group_name",
            "description",
            "group_id",
            *[
                k
                for k in rule.keys()
                if any(keyword in k for keyword in ["trigger_", "action_"])
            ],
        ]:
            del rule[key]
        rule["triggers"] = [
            {k.replace("trigger_", ""): v for k, v in t.items() if "trigger_" in k}
            for t in rule["triggers"]
        ][1:]
        rule["actions"] = [
            {k.replace("action_", ""): v for k, v in a.items() if "action_" in k}
            for a in rule["actions"]
            if a["action_type"] != "set_budget"
        ]
        for trigger in rule["triggers"]:
            trigger["stop_processing"] = False
            trigger["active"] = True
            del trigger["order"]
        for trigger in rule["actions"]:
            trigger["stop_processing"] = False
            trigger["active"] = True
            del trigger["order"]
    return rules


def import_rules(path):
    rules = parse_rules(path)
    for rule in rules:
        jsonschema.validate(
            rule,
            schema["Rule"],
            resolver=jsonschema.RefResolver(base_uri="", referrer="tmp/schema.yaml"),
        )
    for rule in tqdm(rules[1:]):
        post_rule(rule)


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
