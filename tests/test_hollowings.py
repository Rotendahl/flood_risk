import unittest
from PIL import Image
from os import path
from code import address_to_lat_long, address_to_images


class TestHollowings(unittest.TestCase):
    def test_get_img_buildings(self):
        office_address = address_to_lat_long("Jarmers Pl. 2, 1551 København")
        actual_images = address_to_images(coordinates=office_address)
        expected_images = (
            Image.open(
                path.join("tests", "test_images", "get_img_buildings.png")
            ).convert("L"),
            Image.open(
                path.join("tests", "test_images", "get_img_hollowings.png")
            ).convert("L"),
            Image.open(path.join("tests", "test_images", "get_img_map.png")).convert(
                "RGB"
            ),
        )
        self.assertEqual(actual_images, expected_images)


if __name__ == "__main__":
    unittest.main()
