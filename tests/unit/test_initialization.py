import base64
import contextlib
import io
from unittest.mock import Mock, patch

import pytest
from hvac import Client

from hvat import initialization
from hvat.errors import InvalidStateError


class TestInitializeVault:
    vault_init_response = {
        "root_token": "this_is_the_root_token",
        "keys": ["unseal_key_1", "unseal_key_2", "unseal_key_3"],
        "keys_base64": [
            base64.b64encode(b"unseal_key_1"),
            base64.b64encode(b"unseal_key_2"),
            base64.b64encode(b"unseal_key_3"),
        ],
    }

    @pytest.fixture
    def vault_client(self):
        client = Mock(spec=Client)
        client.sys.is_initialized.return_value = False
        client.sys.initialize.return_value = TestInitializeVault.vault_init_response
        return client

    def test_should_throw_invalid_state_error_when_vault_is_initialized(
            self, vault_client
    ):
        vault_client.sys.is_initialized.return_value = True

        with pytest.raises(InvalidStateError, match="Vault is already initialized"):
            initialization.initialize_vault(vault_client)

    def test_should_return_root_token_in_response(self, vault_client):
        result = initialization.initialize_vault(vault_client)

        assert "root_token" in result.keys()
        assert result["root_token"] == self.vault_init_response["root_token"]

    def test_should_return_dict_of_unseal_keys(self, vault_client):
        result = initialization.initialize_vault(vault_client)

        assert "unseal_keys" in result.keys()

    def test_should_return_correct_unseal_keys(self, vault_client):
        result = initialization.initialize_vault(vault_client, shares=3)

        expected_unseal_keys = {
            1: self.vault_init_response["keys"][0],
            2: self.vault_init_response["keys"][1],
            3: self.vault_init_response["keys"][2],
        }
        assert expected_unseal_keys == result["unseal_keys"]

    def test_should_return_correct_encoded_unseal_keys(self, vault_client):
        result = initialization.initialize_vault(vault_client, shares=3)

        expected_unseal_keys = {
            1: self.vault_init_response["keys_base64"][0],
            2: self.vault_init_response["keys_base64"][1],
            3: self.vault_init_response["keys_base64"][2],
        }
        assert expected_unseal_keys == result["unseal_keys_encoded"]


class TestInitAndPush:
    vault_init_response = {
        "root_token": "this_is_the_root_token",
        "keys": ["unseal_key_1", "unseal_key_2", "unseal_key_3"],
        "keys_base64": [
            base64.b64encode(b"unseal_key_1"),
            base64.b64encode(b"unseal_key_2"),
            base64.b64encode(b"unseal_key_3"),
        ],
    }

    @pytest.fixture
    def vault_client(self):
        client = Mock(spec=Client)
        client.sys.is_initialized.return_value = False
        client.sys.initialize.return_value = TestInitializeVault.vault_init_response
        return client

    @patch("hvat.initialization.print_initialization_result")
    def test_should_exit_after_init_when_auto_unseal_enabled(
            self, print_initialization_result, vault_client
    ):
        config = {"init": {"auto_unseal": True}}

        f = io.StringIO()

        with contextlib.redirect_stdout(f):
            initialization.init_and_push(vault_client, config)

        expected = "Auto unseal enabled, please see the relevant stanza in the Vault configuration for details.\n"

        assert expected == f.getvalue()
        print_initialization_result.assert_not_called()

    @patch("hvat.initialization.print_initialization_result")
    def test_should_call_destination_when_auto_unseal_disabled(
            self, print_initialization_result, vault_client
    ):
        config = {"init": {"auto_unseal": False, "destination": {"type": "stdout"}}}

        initialization.init_and_push(vault_client, config)

        print_initialization_result.assert_called_once()
