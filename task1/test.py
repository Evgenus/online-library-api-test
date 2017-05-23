import json
from .factory import Factory
from .evaluation import Evaluator


def parse_and_evaluate(raw_data):
    data = json.loads(raw_data)
    factory = Factory()
    tree = factory.create(data)
    evaluator = Evaluator()
    return evaluator.evaluate(tree)


def test_evaluation_1():
    raw_data = """
    {"operator": "gt", "right": 5, "left": 10}
    """
    assert parse_and_evaluate(raw_data)


def test_evaluation_2():
    raw_data = """
    {"operator": "lt", "right": 5, "left": 1}
    """
    assert parse_and_evaluate(raw_data)


def test_evaluation_sample():
    raw_data = """
    {"operator": "or",
        "right": {"operator": "gt", "right": 5, "left": 10},
        "left": {"operator": "lt", "right": 5, "left": 1}
    }
    """
    assert parse_and_evaluate(raw_data)


def test_evaluation_nested():
    raw_data = """
    {"operator": "and",
        "left": {"operator": "or",
            "right": {"operator": "gt", "right": 5, "left": 10},
            "left": {"operator": "lt", "right": 5, "left": 1}
        },
        "right": {"operator": "ne", "right": 1, "left": 0}
    }
    """
    assert parse_and_evaluate(raw_data)
