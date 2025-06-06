import sys
import types
import os
import json
import unittest
from unittest.mock import patch
import numpy as np

# Provide a minimal torch stub if torch isn't installed
try:
    import torch  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover - for test environment
    torch_stub = types.ModuleType('torch')
    sys.modules['torch'] = torch_stub


class DummyTensor:
    def __init__(self, arr):
        self.arr = arr

    def cpu(self):
        return self

    def numpy(self):
        return self.arr


class TestNSFWGrokDescriber(unittest.TestCase):
    def test_describe_missing_api_key(self):
        from nsfw_grok_describer import NSFWGrokDescriber

        dummy_image = [DummyTensor(np.zeros((1, 1, 3), dtype=np.float32))]

        class DummyResponse:
            status_code = 401
            text = "Unauthorized"

            def json(self):
                return {}

        with patch.dict(os.environ, {}, clear=True), patch('requests.post', return_value=DummyResponse()) as mock_post:
            describer = NSFWGrokDescriber()
            result = describer.describe(dummy_image, "")
            self.assertEqual(result, ("[XAI ERROR 401] Unauthorized",))
            mock_post.assert_called_once()
            headers = mock_post.call_args.kwargs.get('headers', {})
            self.assertEqual(headers.get('Authorization'), 'Bearer missing_key')


class TestNSFWGrokToPonyXL(unittest.TestCase):
    def test_generate_prompts_parses_json(self):
        from nsfw_grok_to_ponyxl import NSFWGrokToPonyXL

        expected = {
            "ponyxl_prompt": "p",
            "wan_prompt": "w",
            "negative_prompt": "n",
            "explanation": "e",
        }

        class DummyResponse:
            status_code = 200

            def raise_for_status(self):
                pass

            def json(self):
                return {"choices": [{"message": {"content": json.dumps(expected)}}]}

        with patch('requests.post', return_value=DummyResponse()) as mock_post:
            node = NSFWGrokToPonyXL()
            result = node.generate_prompts("desc", "key", "motion")
            self.assertEqual(result, ("p", "w", "n", "e"))
            mock_post.assert_called_once()
            headers = mock_post.call_args.kwargs.get('headers', {})
            self.assertEqual(headers.get('Authorization'), 'Bearer key')


if __name__ == '__main__':
    unittest.main()
