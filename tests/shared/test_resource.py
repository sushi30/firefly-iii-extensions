import json
import pytest
from shared.resource import Resource


@pytest.fixture
def example_event():
    with open("../../api_gateway_event_example.json") as f:
        return json.load(f)["input"]


def test_basic_resource(example_event):
    class BasicResource(Resource):
        def get(self):
            return "success"

    BasicResource.handler(example_event, None)
