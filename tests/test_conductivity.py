import unittest
from src.lib import (
    address_to_house_data,
    color_to_conductivity,
    get_conductivity_img,
    get_conductivity_response,
)
from os import path

from PIL import Image


class TestConductivity(unittest.TestCase):
    def test_get_conductivity_img(self):
        office_address = address_to_house_data("Jarmers Pl. 2, 1551 København")[
            "coordinates"
        ]
        actual_image = get_conductivity_img(coordinates=office_address)
        expected_image = Image.open(
            path.join("tests", "test_images", "conductivity_img_office.png")
        ).convert("RGB")

        self.assertEqual(actual_image, expected_image)

    def test_color_to_conductivity(self):
        self.assertEqual(color_to_conductivity([2, 43, 121]), 50)
        self.assertEqual(color_to_conductivity([55, 233, 46]), 725)
        self.assertEqual(color_to_conductivity([228, 124, 49]), 2400)

    def test_get_conductivity_response(self):
        office_address = address_to_house_data("Jarmers Pl. 2, 1551 København")[
            "coordinates"
        ]
        resp = get_conductivity_response(office_address)
        self.assertEqual(resp["value"], 125)
        self.assertEqual(resp["risk"], "high")


if __name__ == "__main__":
    unittest.main()
