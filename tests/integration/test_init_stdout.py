import contextlib
import io
import time

import docker
import pytest
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

        wait = True
        while wait:
            if vault.status == "running":
                wait = False
            else:
                time.sleep(1)
                vault.reload()

        print(client.info())
        print(vault.logs())
        print(vault.status)
        print(vault.diff())
        yield vault

        vault.stop()

    @pytest.fixture
    def vault_client(self, hvat_config):
        return Client(hvat_config["vault_url"])

    def test_should_write_root_token_to_console(self, vault, vault_client, hvat_config):
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            init_and_push(vault_client, hvat_config)

        assert "Root token:" in f.getvalue()

    @pytest.mark.skip(reason="temp disabled")
    def test_should_set_vault_to_initialized(self, vault, vault_client, hvat_config):
        init_and_push(vault_client, hvat_config)

        assert vault_client.sys.is_initialized() is True

    @pytest.mark.skip(reason="temp disabled")
    def test_should_set_vault_to_sealed(self, vault, vault_client, hvat_config):
        init_and_push(vault_client, hvat_config)

        assert vault_client.sys.is_sealed() is True
