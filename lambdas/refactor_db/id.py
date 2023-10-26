from typing import List
from uuid import uuid4

OBJECT_TYPE = [
    'ORG',
    'USER',
    'ROLE',
    'PERM',
]

def generate_id(type: str):
    if type not in OBJECT_TYPE:
        raise Exception(f"Invalid object type: {type}")

    return f'{type}-{uuid4()}'

def is_valid_id(type: str, id: str):
    if type not in OBJECT_TYPE:
        raise Exception(f"Invalid object type: {type}")

    return id.startswith(f"{type}-")
