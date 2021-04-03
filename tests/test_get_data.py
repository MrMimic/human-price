import unittest

from main import convert_scientific_notation

class GetDataTest(unittest.TestCase):

    def test_convert_scientific_notation(self) -> None:
        string = "212×10−25"
        converted = convert_scientific_notation(string)
        self.assertIsInstance(converted, float)

    