import unittest
from unittest.mock import patch, mock_open
from utils.config import save_config, CONFIG_PATH

class TestConfig(unittest.TestCase):
    @patch('utils.config.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_save_config(self, mock_file, mock_json_dump):
        # Arrange
        config_data = {"theme": "dark", "servers": []}

        # Act
        save_config(config_data)

        # Assert
        mock_file.assert_called_once_with(CONFIG_PATH, 'w')
        mock_json_dump.assert_called_once_with(config_data, mock_file(), indent=4)

if __name__ == '__main__':
    unittest.main()
