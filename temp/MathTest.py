import unittest
import math
import MathHandwritten

PRECISION = 1e-9

class MathTest(unittest.TestCase):
    def test1(self):
        base = 10
        exponent = 2

        result = MathHandwritten.pow(base, exponent)
        self.assertEqual(result, 100)

        result *= 0.5
        result += 14
        result = MathHandwritten.squareroot(result)
        self.assertEqual(result, 8)

        f = MathHandwritten.factorial(4)

        self.assertEqual(min(f, result), result)

    def test2(self):
        degree = 34
        radian = 0.593412

        radianTest = MathHandwritten.toRadians(degree)
        degreeTest = MathHandwritten.toDegrees(radian)

        self.assertTrue(abs(radianTest - radian) <= PRECISION)
        self.assertTrue(abs(degree - degreeTest) <= PRECISION)

    def test3(self):
        number = 5
        nlog = MathHandwritten.naturallog(number)
        self.assertTrue(abs(nlog - math.log(number)) <= PRECISION)

        ceiling = MathHandwritten.ceil(nlog)
        self.assertEqual(ceiling, 2)

        p = MathHandwritten.pow(ceiling, ceiling)
        self.assertEqual(p, 4)

        self.assertEqual(min(number, p), p)
        f = MathHandwritten.factorial(5 * 2)
        sqrt = MathHandwritten.squareroot(f)

        self.assertTrue(abs(sqrt - math.sqrt(f)) <= PRECISION)

        p += 24 / 5
        self.assertTrue(abs(MathHandwritten.toRadians(p) - math.radians(p)) <= PRECISION)

if __name__ == '__main__':
    unittest.main()
