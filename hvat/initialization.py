from hvat.stdout import print_initialization_result
from .errors import InvalidStateError
from hvac import Client

DEFAULT_SHARES = 3
DEFAULT_THRESHOLD = 2


def initialize_vault(
    client: Client, shares: int = DEFAULT_SHARES, threshold: int = DEFAULT_THRESHOLD
) -> dict[str, type[str | dict[str, str]]]:
    if client.sys.is_initialized():
        raise InvalidStateError("Vault is already initialized")

    result = client.sys.initialize(secret_shares=shares, secret_threshold=threshold)

    return {
        "root_token": result["root_token"],
        "unseal_keys": {
            index + 1: unseal_key for index, unseal_key in enumerate(result["keys"])
        },
        "unseal_keys_encoded": {
            index + 1: unseal_key
            for index, unseal_key in enumerate(result["keys_base64"])
        },
    }


def init_and_push(client: Client, config: dict):
    vault_result = initialize_vault(client)

    init_config = config["init"]
    if init_config["auto_unseal"]:
        print(
            "Auto unseal enabled, please see the relevant stanza in the Vault configuration for details."
        )
        return

    destinations = {"stdout": print_initialization_result}

    dest = init_config["destination"]["type"]

    destinations[dest](config, vault_result)
