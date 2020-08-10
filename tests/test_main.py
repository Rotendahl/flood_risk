import unittest
import sys


sys.path.insert(0, "./src")

from src.server import app, get_flood_risk  # noqa


class TestRainRisk(unittest.TestCase):
    # executed prior to each test
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()

    def test_get_flood_risk_response(self):
        resp = get_flood_risk("Kjærmarken 103, 6771 gredstedbro")
        self.assertEqual(resp["rain_risk"]["factors"]["basement"]["risk"], "low")
        self.assertEqual(resp["rain_risk"]["factors"]["fastning"]["risk"], "low")
        self.assertEqual(resp["rain_risk"]["factors"]["hollowing"]["risk"], "low")
        self.assertEqual(resp["rain_risk"]["factors"]["conductivity"]["risk"], "low")
        self.assertEqual(resp["rain_risk"]["risk"], "low")
        self.assertEqual(resp["storm_flood"]["risk"], "low")

    def test_handler_address(self):
        resp = self.app.get(
            f"/flood-risk?address={'Jarmers Pl. 2, 1551 København'.replace(' ', '%20')}"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["rain_risk"]["risk"], "medium")
        self.assertEqual(data["navn"], "Jarmers Plads 2, 1551 København V")
        self.assertEqual(data["isAppartment"], False)

    def test_handler_bbr_id(self):
        resp = self.app.get(
            "/flood-risk?unadr_bbrid=40eb1f85-9c53-4581-e044-0003ba298018"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["rain_risk"]["risk"], "low")
        self.assertEqual(data["navn"], "Kjærmarken 103, 6771 Gredstedbro")
        self.assertEqual(data["isAppartment"], False)
