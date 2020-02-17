import os

import requests


def create_budget(budget):
    requests.post(os.environ["ENDPOINT"] + "/")