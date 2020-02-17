from io import StringIO, BytesIO
import boto3
import pandas as pd


def test_s3_file_to_excel():
    bucket = "finance-server.dev.user.files"
    key = "leumicard/transaction-details_export_1563011498725.xlsx"
    excel_file = BytesIO(boto3.resource("s3").Object(bucket, key).get()["Body"].read())
    pd.read_excel(excel_file)
