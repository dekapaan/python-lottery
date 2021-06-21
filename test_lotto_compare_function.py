# Unit test for comparing lotto set and winning numbers
import unittest
from main import LottoFunction
import random
import rsaidnumber
from dateutil import relativedelta
from datetime import datetime


class TestingLottoFunctions(unittest.TestCase):
    def test_compare(self):
        instance = LottoFunction()  # instantiation
        a = [1, 2, 2]
        b = [1, 2, 3]
        self.assertEqual(2, instance.compare(a, b))

    def test_random(self):
        rand_num = random.randint(1, 49)
        self.assertTrue(0 < rand_num < 50, "Random value not in range 1-49")

    def test_rsa_id(self):
        id_pass = rsaidnumber.parse("9811145170081")
        self.assertTrue(id_pass, "ID should return true")

    def test_age(self):
        id_number = rsaidnumber.parse("9811145170081")
        age = relativedelta.relativedelta(datetime.today(), id_number.date_of_birth).years
        self.assertTrue(age >= 18, "Should return true")


if __name__ == '__main__':
    unittest.main()
