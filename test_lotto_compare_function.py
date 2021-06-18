import unittest
from main import LottoFunction


class TestCompare(unittest.TestCase):
    def test_compare(self):
        instance = LottoFunction()
        self.assertEqual(3, instance.compare([1, 2, 3], [1, 2, 3]), " Two Lists of 3 of identical items, should return "
                                                                    "3")


if __name__ == '__main__':
    unittest.main()
