from typing import OrderedDict


def recursive_round(obj):
    if isinstance(obj, OrderedDict):
        return OrderedDict({k: recursive_round(v) for k, v in obj.items()})
    elif isinstance(obj, dict):
        return {k: recursive_round(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [recursive_round(x) for x in obj]
    elif isinstance(obj, float):
        output = round(obj, 2)
        if int(output) == output:
            return int(output)
        return output
    else:
        return obj
