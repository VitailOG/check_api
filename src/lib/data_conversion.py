import json


def json2dict(json_string, remove_key: str):
    data = json.loads(json_string)
    data.pop(remove_key, None)
    return data
