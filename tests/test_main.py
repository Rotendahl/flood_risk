import unittest
import sys
import json

sys.path.insert(0, "./code")  # noqa

from code.app import lambda_handler, get_flood_risk


class TestRainRisk(unittest.TestCase):
    def test_get_flood_risk_response(self):
        resp = json.loads(get_flood_risk("Kjærmarken 103, 6771 gredstedbro"))
        self.assertEqual(resp["rain_risk"]["factors"]["basement"]["risk"], "low")
        self.assertEqual(resp["rain_risk"]["factors"]["fastning"]["risk"], "medium")
        self.assertEqual(resp["rain_risk"]["factors"]["hollowing"]["risk"], "low")
        self.assertEqual(resp["rain_risk"]["factors"]["conductivity"]["risk"], "low")
        self.assertEqual(resp["rain_risk"]["risk"], "low")
        self.assertEqual(resp["storm_flood"]["risk"], "low")

    def test_handler_address(self):
        event = {
            "httpMethod": "GET",
            "queryStringParameters": {"address": "Jarmers Pl. 2, 1551 København"},
        }

        resp = lambda_handler(event, "")
        self.assertEqual(resp["statusCode"], 200)
        data = json.loads(resp["body"])
        self.assertEqual(data["rain_risk"]["risk"], "medium")
        self.assertEqual(data["navn"], "Jarmers Plads 2, 1551 København V")
        self.assertEqual(data["isAppartment"], False)

    def test_handler_bbr_id(self):
        event = {
            "httpMethod": "GET",
            "queryStringParameters": {
                "unadr_bbrid": "40eb1f85-9c53-4581-e044-0003ba298018"
            },
        }
        resp = lambda_handler(event, "")
        self.assertEqual(resp["statusCode"], 200)
        data = json.loads(resp["body"])
        self.assertEqual(data["rain_risk"]["risk"], "low")
        self.assertEqual(data["navn"], "Kjærmarken 103, 6771 Gredstedbro")
        self.assertEqual(data["isAppartment"], False)
