import unittest

from code import get_flood_risk


class TestRainRisk(unittest.TestCase):
    def test_get_flood_risk_response(self):
        resp = get_flood_risk("Kjærmarken 103, 6771 gredstedbro")
        self.assertEqual(resp["rain_risk"]["factors"]["basement"]["risk"], "low")
        self.assertEqual(resp["rain_risk"]["factors"]["fastning"]["risk"], "medium")
        self.assertEqual(resp["rain_risk"]["factors"]["hollowing"]["risk"], "low")
        self.assertEqual(resp["rain_risk"]["factors"]["conductivity"]["risk"], "low")
        self.assertEqual(resp["rain_risk"]["risk"], "low")
        self.assertEqual(resp["storm_flood"]["risk"], "low")
