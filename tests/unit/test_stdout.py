import base64
import contextlib
import io

from hvat.stdout import print_initialization_result


class TestPrintInitializationResult:
    def test_should_print_result_to_stdout(self):
        result = {
            "root_token": "this_is_the_root_token",
            "unseal_keys": {
                "1": "unseal_key_1",
                "2": "unseal_key_2",
                "3": "unseal_key_3"
            },
            "unseal_keys_encoded": {
                "1": f"{base64.b64encode(b'unseal_key_1')}",
                "2": f"{base64.b64encode(b'unseal_key_2')}",
                "3": f"{base64.b64encode(b'unseal_key_3')}"
            }
        }
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            print_initialization_result({}, result)

        assert "Root token: this_is_the_root_token" in f.getvalue()
        assert "1: unseal_key_1" in f.getvalue()
        assert "2: unseal_key_2" in f.getvalue()
        assert "3: unseal_key_3" in f.getvalue()
