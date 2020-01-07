import unittest
from os import path
from PIL import Image
import numpy as np

from code import (
    isolate_building,
    greyscale_to_binary_image,
    combine_images,
    replace_color,
)


class TestImageHandling(unittest.TestCase):
    def test_greyscale_to_binary_image(self):
        greyMatrix = np.random.randint(0, 255, size=(100, 100)).astype(np.uint8)
        colorImage = Image.fromarray(greyMatrix, mode="L")
        greyThreshold = 128

        binary_array = np.asarray(greyscale_to_binary_image(colorImage, greyThreshold))
        self.assertTrue(np.array_equal(binary_array > 0, greyMatrix > greyThreshold))

    def test_isolate_building(self):
        actual_image = isolate_building(
            Image.open(path.join("tests", "test_images", "buildings.png"))
        )

        expected_image = Image.open(
            path.join("tests", "test_images", "isolated_building.png")
        ).convert("1")

        self.assertEqual(actual_image, expected_image)

    def test_combine_images(self):
        verticalImage = np.zeros((100, 100)).astype(np.uint8)
        horizontalImage = np.zeros((100, 100)).astype(np.uint8)
        halfImageLength = int(len(verticalImage) / 2)
        fullImageLength = len(verticalImage)
        verticalImage[0:fullImageLength, 0:halfImageLength] = np.uint8(255)
        horizontalImage[0:halfImageLength, 0:fullImageLength] = np.uint8(255)
        horizontalImage = Image.fromarray(horizontalImage, mode="L")
        verticalImage = Image.fromarray(verticalImage, mode="L")
        combinedImage = np.asarray(combine_images(horizontalImage, verticalImage))
        self.assertTrue(
            np.array_equal(
                combinedImage[0:halfImageLength, 0:halfImageLength],
                np.ones((halfImageLength, halfImageLength)) * 255,
            ),
            msg="Upper left quardrant of image did not match",
        )
        self.assertTrue(
            np.array_equal(
                combinedImage[halfImageLength:, 0:halfImageLength],
                np.ones((halfImageLength, halfImageLength)) * 127,
            ),
            msg="Upper right quardrant of image did not match",
        )
        self.assertTrue(
            np.array_equal(
                combinedImage[0:halfImageLength:, halfImageLength:],
                np.ones((halfImageLength, halfImageLength)) * 127,
            ),
            msg="Lower left quardrant of image did not match",
        )

    def test_replace_color(self):
        color_image = np.ndarray(shape=(100, 100, 4), dtype=np.uint8)
        halfImageLength = int(len(color_image) / 2)
        fullImageLength = len(color_image)
        red = (255, 0, 0, 255)
        green = (0, 255, 0, 255)
        blue = (0, 0, 255, 255)
        color_image[0:halfImageLength, 0:halfImageLength] = red
        color_image[halfImageLength:, 0:halfImageLength] = blue
        color_image[0:fullImageLength, halfImageLength:] = green
        green_image = replace_color(color_image, red, green)
        expected_image = np.ndarray(shape=(100, 100, 4), dtype=np.uint8)
        expected_image[:, :] = green
        expected_image[halfImageLength:, 0:halfImageLength] = blue
        self.assertTrue(np.array_equal(np.asarray(green_image), expected_image))


if __name__ == "__main__":
    unittest.main()
