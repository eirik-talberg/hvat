import base64
import contextlib
import io
import json

from hvat.stdout import print_initialization_result


class TestPrintInitializationResult:
    def test_should_print_result_to_stdout(self):
        result = {
            "root_token": "this_is_the_root_token",
            "keys": ["unseal_key_1", "unseal_key_2", "unseal_key_3"],
            "keys_base64": [
                f"{base64.b64encode(b'unseal_key_1')}",
                f"{base64.b64encode(b'unseal_key_2')}",
                f"{base64.b64encode(b'unseal_key_3')}",
            ],
        }
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            print_initialization_result({}, result)

        expected = f"""VAULT INIT COMPLETE
{json.dumps(result, indent=4)}
PLEASE SAVE THIS INFO SOMEWHERE SAFE
"""

        assert expected == f.getvalue()
