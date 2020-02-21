import csv
import os


def main():
    with open("tmp/files/2020_02_17_rules.csv", encoding="utf8") as fp:
        reader = csv.DictReader(fp)
        records = [r for r in reader]
    rules = []
    for rule in filter(lambda x: x["row_contains"] == "rule", records):
        if rule["row_contains"] == "rule":
            relevant = [r for r in records if r["rule_id"] == rule["rule_id"]]
            triggers = [row for row in relevant if row["row_contains"] == "trigger"]
            actions = [row for row in relevant if row["row_contains"] == "action"]
            rules.append({"rule": rule, "actions": actions, "trigger": triggers})
    bodies = [{"title": 0} for rule in rules]
    print(rules)


if __name__ == "__main__":
    main()

# ENDPOINT = os.environ["ENDPOINT"]


def foo():
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
