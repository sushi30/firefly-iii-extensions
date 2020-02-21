import yaml

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
    with open("tmp/schema.yaml", "r") as fp:
        schema = yaml.load(fp)
        print(schema)
