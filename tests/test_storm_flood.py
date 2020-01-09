import unittest

from PIL import Image
from os import path

from code import (
    get_storm_flood_img,
    address_to_id_and_coordinates,
    get_storm_flod_response,
)


class TestFastning(unittest.TestCase):
    def test_get_flood_img(self):
        _, blox_coordinates = address_to_id_and_coordinates(
            "Bryghusgade, 1473 København"
        )
        actual_image = get_storm_flood_img(blox_coordinates)
        expected_image = Image.open(
            path.join("tests", "test_images", "blox_storm_flood.png")
        )

        self.assertEqual(actual_image, expected_image)

    def test_get_storm_flod_response(self):
        _, blox_coordinates = address_to_id_and_coordinates(
            "Bryghusgade, 1473 København"
        )
        blox_risk = get_storm_flod_response(blox_coordinates)["risk"]
        self.assertEqual(blox_risk, "medium")

        _, DIKU_coordinates = address_to_id_and_coordinates(
            "Universitetsparken 1, 2100 København"
        )
        DIKU_risk = get_storm_flod_response(DIKU_coordinates)["risk"]
        self.assertEqual(DIKU_risk, "low")


#
#     def test_fastning_img_to_value(self):
#         office_address = address_to_lat_long("Kjærmarken 103, 6771 gredstedbro")
#         fastning_image = get_fastning_img(coordinates=office_address)
#         fastning_image_to_value(fastning_image)
#
#         self.assertEqual(fastning_image_to_value(fastning_image), 44.75)
#
#     def test_get_conductivity_response(self):
#         office_address = address_to_lat_long("Jarmers Pl. 2, 1551 København")
#         resp = get_fastning_response(office_address)
#
#         self.assertEqual(resp["value"], 51.53)
#         self.assertEqual(resp["risk"], "high")
#
#
#
# if __name__ == "__main__":
#     unittest.main()
