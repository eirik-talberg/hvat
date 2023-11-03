def print_initialization_result(config: dict, result: dict):
    print("====VAULT INIT COMPLETE====")
    print(f"Root token: {result['root_token']}")
    for key_id, key in result["unseal_keys"].items():
        print(f"Unseal key {key_id}: {key} ({result['unseal_keys_encoded'][key_id]})")
    print("====DONE====")
