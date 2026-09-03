"""Unit tests for KelvraSpace Dashboard."""
import unittest
from fastapi.testclient import TestClient

from src.server import app


class TestKelvraSpace(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["service"], "kelvra-space")
        self.assertEqual(data["port"], 8090)

    def test_overview_structure(self):
        res = self.client.get("/api/overview")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("hub", data)
        self.assertIn("services", data)
        self.assertIn("voice", data["services"])
        self.assertIn("bench", data["services"])
        self.assertIn("security", data["services"])

    def test_index_page(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Kelvra Space", res.text)


if __name__ == "__main__":
    unittest.main()
