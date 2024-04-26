import json
from jsonschema import validate, ValidationError

schema = {
    "type": "object",
    "properties": {
        "price": {"type": "number"},
        "volume": {"type": "number"}
    },
    "required": ["price", "volume"]
}


def validate_data(data):
    try:
        validate(instance=json.loads(data), schema=schema)
    except ValidationError as e:
        raise ValueError(f"Invalid data: {e}")
