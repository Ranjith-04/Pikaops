import asyncio
import unittest
from utils.docker_lib import list_containers
from utils.metrics import get_local_metrics
from utils.k8s_lib import list_k8s_scripts, get_scripts_dir
import os

class TestPikaOpsUtils(unittest.IsolatedAsyncioTestCase):
    async def test_docker_list_containers(self):
        # Even if docker isn't installed or running, this should return a list
        # without crashing.
        containers = await list_containers()
        self.assertIsInstance(containers, list)
        if containers:
            keys = containers[0].keys()
            self.assertIn("id", keys)
            self.assertIn("name", keys)
            self.assertIn("state", keys)

    def test_local_metrics(self):
        metrics = get_local_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn("cpu", metrics)
        self.assertIn("memory", metrics)
        self.assertIn("disk", metrics)
        self.assertIn("network", metrics)

    def test_k8s_scripts_dir(self):
        scripts_dir = get_scripts_dir()
        self.assertTrue(os.path.exists(scripts_dir))

    def test_k8s_list_scripts(self):
        scripts = list_k8s_scripts()
        self.assertIsInstance(scripts, list)

if __name__ == '__main__':
    unittest.main()
