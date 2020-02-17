import boto3

from parsers.leumicard_parser import LeumiCardParser


def process_new_file(event, context):
    for record in event["Records"]:
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        obj = boto3.resource("s3").object(bucket, key).get()
        lcp = LeumiCardParser(obj).parse()
        boto3.resource("s3").object(bucket, "ready/" + key.split("/")[1]).put(
            lcp.dumps()
        )
