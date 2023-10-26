import pytest
import yaml
from hvat.config import read_config, validate_init_config
from hvat.errors import ConfigError


class TestReadConfig:
    def test_read_config(self):
        with open("tests/config_stdout.yaml") as file:
            expected = yaml.safe_load(file)

        result = read_config("tests/config_stdout.yaml")

        assert result == expected


class TestValidateInitConfig:
    def test_should_raise_ConfigError_when_auto_unseal_is_missing(self):
        invalid_config = {}

        with pytest.raises(
            ConfigError,
            match="Missing 'auto_unseal' option in configuration file. Please specify",
        ):
            validate_init_config(invalid_config)

    def test_should_allow_auto_unseal_as_only_option(self):
        valid_config = {"auto_unseal": True}

        validate_init_config(valid_config)

    def test_should_raise_ConfigError_when_destination_is_missing(self):
        invalid_config = {
            "auto_unseal": False,
        }

        with pytest.raises(
            ConfigError,
            match="Missing 'destination' section in configuration file. This must be specified when 'auto_unseal'"
            + " is False.",
        ):
            validate_init_config(invalid_config)

    def test_should_raise_ConfigError_when_type_is_missing_in_destination(self):
        invalid_config = {"auto_unseal": False, "destination": {}}

        with pytest.raises(
            ConfigError,
            match="Missing 'type' in 'destination section' in configuration file.",
        ):
            validate_init_config(invalid_config)
