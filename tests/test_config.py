import unittest
from unittest.mock import patch, mock_open
import json

from utils.config import load_config, DEFAULT_CONFIG

class TestConfig(unittest.TestCase):

    @patch('utils.config.os.path.exists')
    @patch('utils.config.save_config')
    def test_load_config_file_missing(self, mock_save_config, mock_exists):
        # Setup: file does not exist
        mock_exists.return_value = False

        # Action
        result = load_config()

        # Verify
        mock_exists.assert_called_once_with("config.json")
        mock_save_config.assert_called_once_with(DEFAULT_CONFIG)
        self.assertEqual(result, DEFAULT_CONFIG)

    @patch('utils.config.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='{"theme": "dark", "servers": [{"name": "test"}]}')
    def test_load_config_valid_json(self, mock_file, mock_exists):
        # Setup: file exists
        mock_exists.return_value = True

        # Action
        result = load_config()

        # Verify
        mock_exists.assert_called_once_with("config.json")
        mock_file.assert_called_once_with("config.json", "r")
        self.assertEqual(result, {"theme": "dark", "servers": [{"name": "test"}]})

    @patch('utils.config.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json text {')
    def test_load_config_invalid_json(self, mock_file, mock_exists):
        # Setup: file exists but invalid content
        mock_exists.return_value = True

        # Action
        result = load_config()

        # Verify
        mock_exists.assert_called_once_with("config.json")
        mock_file.assert_called_once_with("config.json", "r")
        # Should catch exception and return default config
        self.assertEqual(result, DEFAULT_CONFIG)

if __name__ == '__main__':
    unittest.main()
