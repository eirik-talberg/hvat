import json


def print_initialization_result(config: dict, result: dict):
    print("VAULT INIT COMPLETE")
    print(json.dumps(result, indent=4))
    print("PLEASE SAVE THIS INFO SOMEWHERE SAFE")
