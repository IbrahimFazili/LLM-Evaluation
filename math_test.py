import unittest
from math import log, sqrt, ceil, radians, degrees

"""ADDED LATER:"""
import java
Math = java.type('org.cornell.Math')
""""""

class MathTest(unittest.TestCase):
    PRECISION = 1e-9

    def test1(self):
        base = 10
        exponent = 2

        result = pow(base, exponent)
        self.assertAlmostEqual(result, 100)

        result *= 0.5
        result += 14
        result = sqrt(result)
        self.assertAlmostEqual(result, 8)

        f = self.factorial(4)

        self.assertAlmostEqual(min(f, result), result)

    def test2(self):
        degree = 34
        radian = 0.593412

        radianTest = radians(degree)
        degreeTest = degrees(radian)

        self.assertAlmostEqual(abs(radianTest - radian), 0, delta=self.PRECISION)
        self.assertAlmostEqual(abs(degree - degreeTest), 0, delta=self.PRECISION)

    def test3(self):
        number = 5
        nlog = self.naturallog(number)
        self.assertAlmostEqual(abs(nlog - log(number)), 0, delta=self.PRECISION)

        ceiling = ceil(nlog)
        self.assertAlmostEqual(ceiling, 2)

        p = pow(ceiling, ceiling)
        self.assertAlmostEqual(p, 4)

        self.assertAlmostEqual(min(number, p), p)
        f = self.factorial(5 * 2)
        sqrt_value = sqrt(f)

        self.assertAlmostEqual(abs(sqrt_value - sqrt(f)), 0, delta=self.PRECISION)

        p += 24 / 5
        self.assertAlmostEqual(abs(radians(p) - radians(p)), 0, delta=self.PRECISION)

    def naturallog(self, x):
        return log(x)

    def factorial(self, n):
        if n == 0:
            return 1
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result
