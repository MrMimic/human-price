import os
import sys
import unittest

src_folder = os.path.join("src", "python")
sys.path.append(src_folder)

from utilities import average_range, convert_scientific_notation

class GetDataTest(unittest.TestCase):

    def test_convert_scientific_notation(self) -> None:
        string = "212×10−25"
        converted = convert_scientific_notation(string)
        self.assertIsInstance(converted, float)

    def test_average_range(self) -> None:
        string = "212×10−1–212×10−2"
        converted = average_range(string)
        self.assertIsInstance(converted, float)
