import json
from pathlib import Path

import jsonschema


def get_schema(path_str):
    schema_path = Path(path_str)
    with schema_path.open("r", encoding="utf8") as stream:
        return json.load(stream)

DEFAULT_SCHEMA = get_schema(str(Path(__file__).parent.joinpath("schema.json")))


def validate(raw_data):
    data = json.loads(raw_data)
    jsonschema.validate(data, DEFAULT_SCHEMA)
