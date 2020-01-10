import unittest
from PIL import Image
from os import path

from code import (
    address_to_id_and_coordinates,
    bounding_box,
    get_satelite_img,
    get_basement_response,
)


class TestDataRetrieval(unittest.TestCase):
    def test_address_to_id_and_coordinates(self):
        id, coordinates = address_to_id_and_coordinates("Jarmers Pl. 2, 1551 København")
        self.assertAlmostEqual(
            coordinates, (55.67946496, 12.56466489),
        )
        self.assertEqual(id, "0a3f507a-9dcc-32b8-e044-0003ba298018")

    def test_bounding_box_size(self):
        box = bounding_box((0, 0), boxSize=200, ESPG="3857")
        self.assertEqual(box, "-100.0,-100.0,100.0,100.0")

    def test_bounding_box_espg_3857(self):
        _, coordinates = address_to_id_and_coordinates("Jarmers Pl. 2, 1551 København")
        box = bounding_box(coordinates, boxSize=200, ESPG="3857")
        self.assertEqual(
            box,
            "1398592.0975429227,7494769.030811637,1398792.0975429227,7494969.030811637",
        )

    def test_has_basement(self):
        no_basement_id, _ = address_to_id_and_coordinates(
            "Kjærmarken 103, 6771 gredstedbro"
        )
        basement_id, _ = address_to_id_and_coordinates("Kiærsvej 2, 6760 Ribe")
        self.assertEqual(get_basement_response(no_basement_id)["risk"], "low")
        self.assertEqual(get_basement_response(basement_id)["risk"], "high")

    def test_bounding_box_espg_25832(self):
        _, coordinates = address_to_id_and_coordinates(
            "Kjærmarken 103, 6771 Gredstedbro"
        )
        box = bounding_box(coordinates, ESPG="25832")
        self.assertEqual(
            box,
            "483622.5205332278,6139451.855766358,483736.7176466355,6139564.964581124",
        )

    def test_get_satelite_img(self):
        _, office_address = address_to_id_and_coordinates(
            "Jarmers Pl. 2, 1551 København"
        )
        actual_image = get_satelite_img(office_address)
        expected_image = Image.open(
            path.join("tests", "test_images", "get_img_map.png")
        ).convert("RGB")
        self.assertEqual(actual_image, expected_image)


if __name__ == "__main__":
    unittest.main()
