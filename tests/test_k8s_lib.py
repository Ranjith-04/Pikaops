import os
import unittest
from unittest.mock import patch
from utils.k8s_lib import get_scripts_dir

class TestK8sLib(unittest.TestCase):
    @patch('utils.k8s_lib.os.path.abspath')
    @patch('utils.k8s_lib.os.makedirs')
    @patch('utils.k8s_lib.os.path.exists')
    def test_get_scripts_dir_exists(self, mock_exists, mock_makedirs, mock_abspath):
        mock_abspath.return_value = '/fake/project/utils/k8s_lib.py'
        mock_exists.return_value = True

        expected_dir = os.path.join('/fake/project', 'scripts', 'k8s')
        result_dir = get_scripts_dir()

        self.assertEqual(result_dir, expected_dir)
        mock_makedirs.assert_not_called()

    @patch('utils.k8s_lib.os.path.abspath')
    @patch('utils.k8s_lib.os.makedirs')
    @patch('utils.k8s_lib.os.path.exists')
    def test_get_scripts_dir_not_exists(self, mock_exists, mock_makedirs, mock_abspath):
        mock_abspath.return_value = '/fake/project/utils/k8s_lib.py'
        mock_exists.return_value = False

        expected_dir = os.path.join('/fake/project', 'scripts', 'k8s')
        result_dir = get_scripts_dir()

        self.assertEqual(result_dir, expected_dir)
        mock_makedirs.assert_called_once_with(expected_dir)

if __name__ == '__main__':
    unittest.main()
