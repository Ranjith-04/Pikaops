import pytest
from utils.docker_lib import manage_container

@pytest.mark.asyncio
async def test_manage_container_invalid_action():
    success, message = await manage_container("test_id", "invalid_action")
    assert success is False
    assert message == "Invalid action"
