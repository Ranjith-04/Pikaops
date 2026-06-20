import os
import json
from unittest.mock import patch, mock_open

from utils.config import load_config, DEFAULT_CONFIG

def test_load_config_file_exists():
    mock_data = '{"servers": [{"name": "test", "ip": "1.1.1.1"}], "theme": "pika"}'
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=mock_data)):
            config = load_config()
            assert config == {"servers": [{"name": "test", "ip": "1.1.1.1"}], "theme": "pika"}

def test_load_config_file_not_exists():
    with patch("os.path.exists", return_value=False):
        with patch("utils.config.save_config") as mock_save:
            config = load_config()
            assert config == DEFAULT_CONFIG
            mock_save.assert_called_once_with(DEFAULT_CONFIG)

def test_load_config_invalid_json():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data="invalid json")):
            config = load_config()
            assert config == DEFAULT_CONFIG

def test_load_config_io_error():
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", side_effect=IOError("Test Error")):
            config = load_config()
            assert config == DEFAULT_CONFIG
