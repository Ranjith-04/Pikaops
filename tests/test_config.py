import pytest
from unittest.mock import patch
from utils.config import add_server

@patch('utils.config.load_config')
@patch('utils.config.save_config')
def test_add_server(mock_save_config, mock_load_config):
    # Setup mock config
    mock_config = {
        "servers": [
            {
                "name": "Existing-Server",
                "ip": "10.0.0.2",
                "user": "olduser",
                "exporter_url": "http://10.0.0.2:9100/metrics"
            }
        ],
        "theme": "pika"
    }
    mock_load_config.return_value = mock_config

    # Call the function
    add_server("Test-Server", "10.0.0.1", "testuser", "http://10.0.0.1:9100/metrics")

    # Assert load_config was called
    mock_load_config.assert_called_once()

    # Assert save_config was called with the updated config
    expected_config = {
        "servers": [
            {
                "name": "Existing-Server",
                "ip": "10.0.0.2",
                "user": "olduser",
                "exporter_url": "http://10.0.0.2:9100/metrics"
            },
            {
                "name": "Test-Server",
                "ip": "10.0.0.1",
                "user": "testuser",
                "exporter_url": "http://10.0.0.1:9100/metrics"
            }
        ],
        "theme": "pika"
    }
    mock_save_config.assert_called_once_with(expected_config)
