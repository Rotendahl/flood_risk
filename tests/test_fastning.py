import unittest
import base64

from PIL import Image
from os import path
from io import BytesIO

import numpy as np

from code import (
    get_fastning_img,
    address_to_id_and_coordinates,
    fastning_image_to_value,
    get_fastning_response,
)


class TestFastning(unittest.TestCase):
    def test_get_fastning_img(self):
        _, office_address = address_to_id_and_coordinates(
            "Jarmers Pl. 2, 1551 København"
        )
        actual_image = get_fastning_img(coordinates=office_address)
        expected_image = Image.open(
            path.join("tests", "test_images", "get_fastning_office.png")
        ).convert("RGB")

        self.assertEqual(actual_image, expected_image)

    def test_fastning_img_to_value(self):
        _, office_address = address_to_id_and_coordinates(
            "Kjærmarken 103, 6771 gredstedbro"
        )
        fastning_image = get_fastning_img(coordinates=office_address)
        fastning_image_to_value(fastning_image)

        self.assertEqual(fastning_image_to_value(fastning_image), 44.75)

    def test_get_conductivity_response_high(self):
        _, office_address = address_to_id_and_coordinates(
            "Jarmers Pl. 2, 1551 København"
        )
        resp = get_fastning_response(office_address)

        self.assertEqual(resp["value"], 51.53)
        self.assertEqual(resp["risk"], "high")

        actual_image = np.asarray(Image.open(BytesIO(base64.b64decode(resp["image"]))))
        expected_image = np.asarray(
            Image.open(
                path.join("tests", "test_images", "fastning_map_office.png")
            ).convert("RGB")
        )
        self.assertTrue(np.allclose(actual_image, expected_image, atol=1))

    def test_get_conductivity_response_medium(self):
        _, home_coordinates = address_to_id_and_coordinates(
            "Kjærmarken 103, 6771 gredstedbro"
        )
        resp = get_fastning_response(home_coordinates)

        self.assertEqual(resp["risk"], "medium")
        self.assertEqual(resp["value"], 44.75)


if __name__ == "__main__":
    unittest.main()
