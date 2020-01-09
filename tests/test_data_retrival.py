import unittest
from PIL import Image
from os import path

from code import address_to_lat_long, bounding_box, get_satelite_img


class TestDataRetrieval(unittest.TestCase):
    def test_address_to_lat_long(self):
        self.assertAlmostEqual(
            address_to_lat_long("Jarmers Pl. 2, 1551 København"),
            (55.67946496, 12.56466489),
        )

    def test_bounding_box_size(self):
        box = bounding_box((0, 0), boxSize=200, ESPG="3857")
        self.assertEqual(box, "-100.0,-100.0,100.0,100.0")

    def test_bounding_box_espg_3857(self):
        coordinates = address_to_lat_long("Jarmers Pl. 2, 1551 København")
        box = bounding_box(coordinates, boxSize=200, ESPG="3857")
        self.assertEqual(
            box,
            "1398592.0975429227,7494769.030811637,1398792.0975429227,7494969.030811637",
        )

    # def test_bounding_box_espg_25832(self):
    #     coordinates = address_to_lat_long("Kjærmarken 103, 6771 Gredstedbro")
    #     box = bounding_box(coordinates, ESPG="25832")
    #     self.assertEqual(
    #         box,
    #         "483566.4996201384,6139409.830860353,483792.73496987607,6139606.992386308",
    #     )

    def test_get_satelite_img(self):
        office_address = address_to_lat_long("Jarmers Pl. 2, 1551 København")
        actual_image = get_satelite_img(office_address)
        expected_image = Image.open(
            path.join("tests", "test_images", "get_img_map.png")
        ).convert("RGB")
        self.assertEqual(actual_image, expected_image)


if __name__ == "__main__":
    unittest.main()
