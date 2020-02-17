import json
from abc import ABC


class Parser(ABC):
    def __init__(self):
        self.rows = []

    def transactions_as_dict(self):
        return [t.to_dict() for t in self.transactions]

    def parser(self,):
        pass

    def from_string(self):
        pass

    def dumps(self, *args, **kwargs):
        return json.dumps(self.rows, *args, **kwargs)
