import base64
import json
import boto3


def get_secret(secret_id: str):
    secrets_manager = boto3.client("secretsmanager")
    get_secret_value_response = secrets_manager.get_secret_value(SecretId=secret_id)
    if "SecretString" in get_secret_value_response:
        secret = get_secret_value_response["SecretString"]
    else:
        secret = base64.b64decode(get_secret_value_response["SecretBinary"])
    return json.loads(secret)
