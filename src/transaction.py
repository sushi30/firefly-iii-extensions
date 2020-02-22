import os
import requests

from src.api_calls import response_wrapper


class Transaction:
    def __init__(self, _id, **attributes):
        self.id = _id
        self.attributes = attributes

    def delete(self):
        return response_wrapper(
            requests.delete(
                os.environ["ENDPOINT"] + "/api/v1/transactions/" + self.id,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + os.environ["TOKEN"],
                },
            )
        )
