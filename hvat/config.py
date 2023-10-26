import yaml

from hvat.errors import ConfigError


def read_config(path: str) -> dict:
    with open(path, "r") as f:
        config = yaml.safe_load(f)

    if "init" in config.keys():
        validate_init_config(config["init"])

    return config


def validate_init_config(config: dict):
    if "auto_unseal" not in config.keys():
        raise ConfigError(
            "Missing 'auto_unseal' option in configuration file. Please specify"
        )

    if config["auto_unseal"] is True:
        return

    if "destination" not in config.keys():
        raise ConfigError(
            "Missing 'destination' section in configuration file. This must be specified when 'auto_unseal' is False."
        )

    destination = config["destination"]

    if "type" not in destination.keys():
        raise ConfigError(
            "Missing 'type' in 'destination section' in configuration file."
        )

    if destination["type"] == "stdout":
        return
