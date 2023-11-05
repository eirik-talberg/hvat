import contextlib
import io
import time

import docker
import pytest
import urllib3.exceptions
from docker.models.containers import Container
from from_root import from_root
from hvac import Client

from hvat.initialization import init_and_push


class TestInitWithStdout:

    @pytest.fixture
    def vault_port(self) -> int:
        return 8200

    @pytest.fixture
    def hvat_config(self, vault_port: int) -> dict:
        return {
            "vault_url": f"http://localhost:{vault_port}",
            "init": {
                "auto_unseal": False,
                "destination": {
                    "type": "stdout"
                }
            }
        }

    @pytest.fixture
    def vault(self, vault_port: int) -> Container:
        client = docker.from_env()
        config = {
            "cap_add": [
                "IPC_LOCK"
            ],
            "ports": {
                "8200": f"{vault_port}"
            },
            "volumes": [
                f"{from_root()}/vault/configs/:/vault/config"
            ],
            "detach": True,
            "auto_remove": True
        }
        vault = client.containers.run("hashicorp/vault:1.14.4", "server", **config)

        while vault.status != "running":
            print("Container is not ready. Sleeping for 0.5s")
            time.sleep(0.5)
            vault.reload()

        yield vault

        vault.stop()

    @pytest.fixture
    def vault_client(self, hvat_config, vault):
        client = Client(hvat_config["vault_url"])

        status = 0
        while status != 501:
            try:
                status = client.sys.read_health_status().status_code
            except urllib3.exceptions.ConnectionError as e:
                print(e)
                print("Vault is not ready. Sleeping for 0.5s")
                time.sleep(0.5)

        return client

    def test_should_write_root_token_to_console(self, vault, vault_client, hvat_config):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            init_and_push(vault_client, hvat_config)

        assert "Root token:" in f.getvalue()

    def test_should_set_vault_to_initialized(self, vault, vault_client, hvat_config):
        init_and_push(vault_client, hvat_config)

        assert vault_client.sys.is_initialized() is True

    def test_should_set_vault_to_sealed(self, vault, vault_client, hvat_config):
        init_and_push(vault_client, hvat_config)

        assert vault_client.sys.is_sealed() is True
