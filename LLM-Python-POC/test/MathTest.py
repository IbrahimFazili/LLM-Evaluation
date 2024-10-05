import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from Math import Math

class MathTest(unittest.TestCase):

    def test1(self):
        base = 10
        exponent = 2

        result = Math.pow(base, exponent)
        self.assertEqual(result, 100)

        result *= 0.5
        result += 14

        result = Math.squareroot(result)
        self.assertEqual(result, 8)

        f = Math.factorial(4)

        self.assertEqual(Math.min(f, result), result)

    def test2(self):
        degree = 34
        radian = 0.593412

        radianTest = Math.toRadians(degree)
        degreeTest = Math.toDegrees(radian)

        self.assertLessEqual(Math.abs(radianTest - radian), Math.PRECISION)
        self.assertLessEqual(Math.abs(degreeTest - degree), Math.PRECISION)

    def test3(self):
        pass

if __name__ == '__main__':
    unittest.main()
