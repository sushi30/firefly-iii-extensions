import json
import logging
from datetime import datetime
from io import BytesIO
import boto3
import pandas as pd
from app import LOG_LEVEL

log = logging.getLogger(__name__)
log.setLevel(LOG_LEVEL)

# noinspection PyTypeChecker
def get_fibi(path):
    df = pd.read_excel("data/" + path)
    df = df[df.columns[[3, 4, 5, 8]]]
    df.columns = ["plus", "minus", "name", "date"]
    df = df.iloc[3:]
    df["value"] = df.plus.apply(lambda x: 0 if type(x) == str else x) - df.minus.apply(
        lambda x: 0 if type(x) == str else x
    )
    df = df.reset_index()
    df = df.drop(columns=["plus", "minus", "index"])
    df = df[["date", "name", "value"]]
    df = df[~df.name.apply(lambda x: "ישראכרט" in x)]
    df["source"] = "fibi"
    return df


# noinspection PyTypeChecker
def get_leumicard(bucket, key):
    log.debug("received path: " + str((bucket, key)))
    dfs = []
    for i in [0, 1]:
        excel_file = BytesIO(
            boto3.resource("s3").Object(bucket, key).get()["Body"].read()
        )
        temp = pd.read_excel(excel_file, header=3, sheet_name=i)
        temp = temp[temp.columns[[0, 1, 5, 10]]]
        temp.columns = ["date", "name", "value", "details"]
        dfs.append(temp)
    df = pd.concat(dfs)
    df.date = pd.to_datetime(df.date)
    df = df[["date", "name", "value", "details"]]
    df["source"] = "leumicard"
    df["details"] = df.details.apply(lambda x: "" if pd.isna(x) else x)
    df.value = -df.value
    return df


# noinspection PyTypeChecker
def get_isracard(path):
    df = pd.read_excel("data/" + path)
    indices = df[df[df.columns[0]].apply(str).apply(lambda x: "תאריך" in x)].index
    df1 = df.iloc[indices[0] + 1 : indices[1]]
    df1 = df1[df1.columns[[0, 1, 4, 7]]]
    df1.columns = ["date", "name", "value", "details"]
    df2 = df.iloc[indices[1] + 1 :]
    df2 = df2[df2.columns[[0, 2, 5]]]
    df2.columns = ["date", "name", "value"]
    df2 = df2[~df2.name.apply(str).apply(lambda x: "TOTAL" in x)]
    df = (
        pd.concat([df1, df2], ignore_index=True, sort=False)
        .reset_index()
        .drop(columns=["index"])
    )
    df.date = pd.to_datetime(df.date, dayfirst=True, errors="coerce")
    df.value = pd.to_numeric(df.value, errors="coerce")
    df = df[["date", "name", "value", "details"]]
    df = df.dropna(subset=["date", "name", "value"])
    df.value = -df.value
    df["source"] = "isracard"
    return df


def categorize(string):
    with open("categories.json", encoding="utf-8") as f:
        categories = json.load(f)
    for i, j in categories.items():
        if any(k in string for k in j):
            return i
    return None


def get_leumi(path):
    def parse_date(x):
        if type(x) == type(""):
            return datetime.strptime(x, "%d/%m/%y")
        else:
            return datetime(x.year, x.day, x.month)

    df = pd.read_excel("data/" + path)
    df = df[df.columns[[0, 1, 3, 4]]]
    df.columns = ["date", "name", "minus", "plus"]
    df["value"] = df.plus.fillna(0) - df.minus.fillna(0)
    df = df.reset_index()
    df = df.drop(columns=["plus", "minus", "index"])
    df = df[["date", "name", "value"]]
    df.date = df.date.apply(parse_date)
    for w in ["ויזה", "מאוצר החייל", "העברה עצמית", "מס הכנסה", "רבית זכות"]:
        df = df[~df.name.apply(lambda x: w in x)]
    df["source"] = "leumi"
    return df


def create_persistence():
    pd.DataFrame([[pd.Timestamp(0), True]], columns=["save_date", "v"]).set_index(
        "save_date"
    ).to_csv("persistence.csv")
