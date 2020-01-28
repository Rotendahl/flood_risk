import unittest
from code.lib import address_to_id_and_coordinates, get_rain_risk_response


class TestRainRisk(unittest.TestCase):
    def test_get_rain_risk_response_1(self):
        address_id, coordinates = address_to_id_and_coordinates(
            "Kjærmarken 103, 6771 gredstedbro"
        )
        resp = get_rain_risk_response(address_id, coordinates)
        self.assertEqual(resp["factors"]["basement"]["risk"], "low")
        self.assertEqual(resp["factors"]["fastning"]["risk"], "medium")
        self.assertEqual(resp["factors"]["hollowing"]["risk"], "low")
        self.assertEqual(resp["factors"]["conductivity"]["risk"], "low")
        self.assertEqual(resp["risk"], "low")

    def test_get_rain_risk_response_2(self):
        address_id, coordinates = address_to_id_and_coordinates(
            "Dronning Dagmars Vej 13, 6760 Ribe"
        )
        resp = get_rain_risk_response(address_id, coordinates)
        self.assertEqual(resp["factors"]["basement"]["risk"], "high")
        self.assertEqual(resp["factors"]["fastning"]["risk"], "high")
        self.assertEqual(resp["factors"]["hollowing"]["risk"], "high")
        self.assertEqual(resp["factors"]["conductivity"]["risk"], "low")
        self.assertEqual(resp["risk"], "high")
