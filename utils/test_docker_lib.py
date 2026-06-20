import unittest
from unittest.mock import patch, MagicMock, AsyncMock
from utils.docker_lib import manage_container

class TestDockerLib(unittest.IsolatedAsyncioTestCase):

    @patch('utils.docker_lib.asyncio.create_subprocess_exec')
    async def test_manage_container_valid(self, mock_create_subprocess_exec):
        mock_proc = MagicMock()
        mock_proc.communicate = AsyncMock(return_value=(b'stdout', b'stderr'))
        mock_proc.returncode = 0
        mock_create_subprocess_exec.return_value = mock_proc

        success, message = await manage_container("valid123", "start")
        self.assertTrue(success)
        self.assertEqual(message, "Container started successfully.")
        mock_create_subprocess_exec.assert_called_once_with(
            "docker", "start", "valid123",
            stdout=unittest.mock.ANY,
            stderr=unittest.mock.ANY
        )

    async def test_manage_container_invalid_action(self):
        success, message = await manage_container("valid123", "invalid_action")
        self.assertFalse(success)
        self.assertEqual(message, "Invalid action")

    @patch('utils.docker_lib.asyncio.create_subprocess_exec')
    async def test_manage_container_invalid_id(self, mock_create_subprocess_exec):
        success, message = await manage_container("invalid-id; ls -la", "start")
        self.assertFalse(success)
        self.assertEqual(message, "Invalid container ID")
        mock_create_subprocess_exec.assert_not_called()

if __name__ == '__main__':
    unittest.main()
