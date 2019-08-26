import unittest
import numpy

from ..hollowings import checkHollowing
from ..data_retrival import addressToLatLong


class TestHollowings(unittest.TestCase):
    def test_address_retrival(self):
        x, y = addressToLatLong("Kjærmarken 103, 6771 Gredstedbro")
        assert x == 55.40156089
        assert y == 8.74228813

        self.assertEqual((x, y), (55.40156089, 8.74228813))

    # Simple smoke test to see if it runs
    def test_hollowing(self):
        count, img = checkHollowing("kjærmarken 103, 6771")
        self.assertEqual(type(count), numpy.int64)


if __name__ == "__main__":
    unittest.main()
