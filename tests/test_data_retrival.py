import unittest
from PIL import Image
from os import path

from code import address_to_lat_long, convert_espg, bounding_box, get_img


class TestDataRetrieval(unittest.TestCase):
    def test_address_to_lat_long(self):
        self.assertAlmostEqual(
            address_to_lat_long("Jarmers Pl. 2, 1551 København"),
            (55.67946496, 12.56466489),
        )

    def test_convert_EPSG(self):
        office_coordinates_4326 = (55.67946496, 12.56466489)
        office_coordinates_3857 = (1398692.0975429227, 7494869.030811637)
        self.assertEqual(
            convert_espg(office_coordinates_4326), office_coordinates_3857,
        )

    def test_bounding_box(self):
        box = bounding_box((100, 100), boxSize=200)
        self.assertEqual(box, "0.0,0.0,200.0,200.0")

    def test_get_img_building(self):
        office_address = address_to_lat_long("Jarmers Pl. 2, 1551 København")
        actual_image = get_img(office_address, "buildings")
        expected_image = Image.open(
            path.join("tests", "test_images", "get_img_buildings.png")
        ).convert("L")
        self.assertEqual(actual_image, expected_image)

    def test_get_img_hollowings(self):
        office_address = address_to_lat_long("Jarmers Pl. 2, 1551 København")
        actual_image = get_img(office_address, "hollowings")
        expected_image = Image.open(
            path.join("tests", "test_images", "get_img_hollowings.png")
        ).convert("L")
        self.assertEqual(actual_image, expected_image)

    def test_get_img_map(self):
        office_address = address_to_lat_long("Jarmers Pl. 2, 1551 København")
        actual_image = get_img(office_address, "map", mode="RGBA")
        expected_image = Image.open(
            path.join("tests", "test_images", "get_img_map.png")
        ).convert("RGBA")
        self.assertEqual(actual_image, expected_image)


if __name__ == "__main__":
    unittest.main()
