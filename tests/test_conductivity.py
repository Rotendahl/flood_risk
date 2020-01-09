import unittest

from PIL import Image
from os import path

from code import (
    address_to_lat_long,
    get_conductivity_img,
    color_to_conductivity,
    get_conductivity_response,
)


class TestConductivity(unittest.TestCase):
    def test_get_conductivity_img(self):
        office_address = address_to_lat_long("Jarmers Pl. 2, 1551 København")
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
        office_address = address_to_lat_long("Jarmers Pl. 2, 1551 København")
        resp = get_conductivity_response(office_address)
        self.assertEqual(resp["value"], 125)
        self.assertEqual(resp["risk"], "high")


if __name__ == "__main__":
    unittest.main()
