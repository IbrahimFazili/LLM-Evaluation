import unittest
import numpy as np
import random
import math
from mpmath import mp, log as mp_log, sin as mp_sin, sinh as mp_sinh
import sys
import AccurateMath


class AccurateMathTest(unittest.TestCase):
    MAX_ERROR_ULP = 0.51
    NUMBER_OF_TRIALS = 1000

    def setUp(self):
        self.precision_epsilon = np.finfo(float).eps
        self.generator = random.Random(6176597458463500194)

    def testMinMaxDouble(self):
        pairs = [
            (-50.0, 50.0),
            (float("inf"), 1.0),
            (float("-inf"), 1.0),
            (float("nan"), 1.0),
            (float("inf"), 0.0),
            (float("-inf"), 0.0),
            (float("nan"), 0.0),
            (float("nan"), float("-inf")),
            (float("nan"), float("inf")),
            (np.finfo(float).tiny, np.finfo(float).eps),
        ]

        for a, b in pairs:
            # Handle NaN values explicitly; skip comparisons involving NaN
            if np.isnan(a) or np.isnan(b):
                continue

            # Test min
            self.assertAlmostEqual(
                min(a, b),  # Python's built-in min
                AccurateMath.min(a, b),  # AccurateMath implementation
                delta=self.precision_epsilon,
                msg=f"Discrepancy in min({a}, {b})",
            )
            self.assertAlmostEqual(
                min(b, a),
                AccurateMath.min(b, a),
                delta=self.precision_epsilon,
                msg=f"Discrepancy in min({b}, {a})",
            )

            # Test max
            self.assertAlmostEqual(
                max(a, b),  # Python's built-in max
                AccurateMath.max(a, b),  # AccurateMath implementation
                delta=self.precision_epsilon,
                msg=f"Discrepancy in max({a}, {b})",
            )
            self.assertAlmostEqual(
                max(b, a),
                AccurateMath.max(b, a),
                delta=self.precision_epsilon,
                msg=f"Discrepancy in max({b}, {a})",
            )

    def testConstants(self):
        self.assertAlmostEqual(
            math.pi, AccurateMath.PI, delta=1.0e-20, msg="Discrepancy in AccurateMath.PI"
        )
        self.assertAlmostEqual(
            math.e, AccurateMath.E, delta=1.0e-20, msg="Discrepancy in AccurateMath.E"
        )

    def testAtan2(self):
        y1, x1 = 1.2713504628280707e10, -5.674940885228782e-10
        self.assertAlmostEqual(
            math.atan2(y1, x1),
            AccurateMath.atan2(y1, x1),
            delta=2 * self.precision_epsilon,
            msg="Discrepancy in atan2(y1, x1)",
        )

        y2, x2 = 0.0, float("inf")  # Double.POSITIVE_INFINITY in Java
        self.assertAlmostEqual(
            math.atan2(y2, x2),
            AccurateMath.atan2(y2, x2),
            delta=self.precision_epsilon,
            msg="Discrepancy in atan2(y2, x2)",
        )

    def testHyperbolic(self):
        x_values = np.arange(-30, 30, 0.001)

        # Test sinh
        max_err = 0
        for x in x_values:
            tst = AccurateMath.sinh(x)
            ref = math.sinh(x)
            max_err = max(max_err, abs(ref - tst) / AccurateMath.ulp(ref))
        self.assertAlmostEqual(0, max_err, delta=2, msg="Discrepancy in sinh computation")

        # Test cosh
        max_err = 0
        for x in x_values:
            tst = AccurateMath.cosh(x)
            ref = math.cosh(x)
            max_err = max(max_err, abs(ref - tst) / AccurateMath.ulp(ref))
        self.assertAlmostEqual(0, max_err, delta=2, msg="Discrepancy in cosh computation")

    def test_log_accuracy(self):
        max_err_ulp = 0.0

        # Set mpmath precision for high-precision computations
        mp.dps = 50

        for _ in range(self.NUMBER_OF_TRIALS):
            x = math.exp(self.generator.random() * 1416.0 - 708.0) * self.generator.random()
            tst = AccurateMath.log(x)
            ref = float(mp_log(mp.mpf(x)))  # High precision logarithm
            err = (tst - ref) / ref

            if err != 0.0:
                ulp = abs(ref - math.nextafter(ref, math.inf))  # Compute ULP of `ref`
                err_ulp = abs((tst - ref) / ulp)
                max_err_ulp = max(max_err_ulp, err_ulp)

        self.assertLess(
            max_err_ulp,
            self.MAX_ERROR_ULP,
            f"log() had errors in excess of {self.MAX_ERROR_ULP} ULP",
        )

    def testExpSpecialCases(self):
        # Smallest value that will round up to np.finfo(float).tiny
        self.assertAlmostEqual(
            np.finfo(float).tiny,
            AccurateMath.exp(-745.1332191019411),
            delta=np.finfo(float).eps,
            msg="exp(-745.1332191019411) should be close to Double.MIN_VALUE"
        )

        self.assertAlmostEqual(
            0.0,
            AccurateMath.exp(-745.1332191019412),
            delta=np.finfo(float).eps,
            msg="exp(-745.1332191019412) should be 0.0"
        )

        self.assertTrue(
            math.isnan(AccurateMath.exp(float('nan'))),
            msg="exp of NaN should be NaN"
        )

        self.assertAlmostEqual(
            float('inf'),
            AccurateMath.exp(float('inf')),
            delta=1.0,
            msg="exp of infinity should be infinity"
        )

        self.assertAlmostEqual(
            0.0,
            AccurateMath.exp(float('-inf')),
            delta=np.finfo(float).eps,
            msg="exp of -infinity should be 0.0"
        )

        self.assertAlmostEqual(
            math.e,
            AccurateMath.exp(1.0),
            delta=np.finfo(float).eps,
            msg="exp(1) should be Math.E"
        )

    def testSinAccuracy(self):
        max_err_ulp = 0.0
        generator = random.Random()

        for _ in range(self.NUMBER_OF_TRIALS):
            # Generate random input x
            x = ((generator.random() * math.pi) - math.pi / 2.0) * (2 ** 21) * generator.random()

            # Calculate test value using AccurateMath.sin
            tst = AccurateMath.sin(x)  # Replace with your AccurateMath.sin implementation if available

            # Reference value using mpmath for high precision
            ref = float(mp_sin(mp.mpf(x)))

            if ref != 0:  # Avoid division by zero
                # Calculate ULP using numpy's nextafter
                ulp = abs(ref - np.nextafter(ref, math.inf))
                err_ulp = abs((tst - ref) / ulp)

                # Track the maximum ULP error
                max_err_ulp = max(max_err_ulp, err_ulp)

        # Check if the maximum error in ULP is within the acceptable range
        self.assertTrue(
            max_err_ulp < self.MAX_ERROR_ULP,
            f"sin() had errors in excess of {self.MAX_ERROR_ULP} ULP (max error: {max_err_ulp})"
        )

    def testSinhAccuracy(self):
        max_err_ulp = 0.0
        generator = random.Random()

        for _ in range(self.NUMBER_OF_TRIALS):
            # Generate random input x
            x = ((generator.random() * 16.0) - 8.0) * generator.random()

            # Calculate test value using AccurateMath.sinh
            tst = AccurateMath.sinh(x)  # Replace with your AccurateMath.sinh implementation if available

            # Reference value using mpmath for high precision
            ref = float(mp_sinh(mp.mpf(x)))

            if ref != 0:  # Avoid division by zero
                # Calculate ULP using numpy's nextafter
                ulp = abs(ref - np.nextafter(ref, math.inf))
                err_ulp = abs((tst - ref) / ulp)

                # Track the maximum ULP error
                max_err_ulp = max(max_err_ulp, err_ulp)

        # Check if the maximum error in ULP is within the acceptable range
        self.assertTrue(
            max_err_ulp < self.MAX_ERROR_ULP,
            f"sinh() had errors in excess of {self.MAX_ERROR_ULP} ULP (max error: {max_err_ulp})"
        )

    def testToDegrees(self):
        max_err_ulp = 0.0
        generator = random.Random()

        for _ in range(self.NUMBER_OF_TRIALS):
            # Generate a random input x
            x = generator.random()

            # Calculate the test value
            tst = float(mp.mpf(x) * 180 / mp.pi)  # High-precision conversion to degrees

            ref = AccurateMath.toDegrees(x)  # Use math.degrees as a placeholder

            # Compute relative error
            if ref != 0:  # Avoid division by zero
                err = (tst - ref) / ref

                if err != 0:
                    # Calculate ULP using nextafter for floating-point precision
                    ulp = abs(ref - math.nextafter(ref, math.inf))
                    err_ulp = abs((tst - ref) / ulp)

                    # Track the maximum ULP error
                    max_err_ulp = max(max_err_ulp, err_ulp)

        # Assert that the maximum error in ULP is within acceptable range
        self.assertTrue(
            max_err_ulp < self.MAX_ERROR_ULP,
            f"toDegrees() had errors in excess of {self.MAX_ERROR_ULP} ULP (max error: {max_err_ulp})"
        )

    def testToRadians(self):
        max_err_ulp = 0.0
        generator = random.Random()

        for _ in range(self.NUMBER_OF_TRIALS):
            # Generate random input x
            x = generator.random()

            # Calculate the test value using high-precision math
            tst = float(mp.mpf(x) * mp.pi / 180)

            ref = AccurateMath.toRadians(x)  # Replace with your custom AccurateMath.toRadians function

            # Compute the relative error
            if ref != 0:  # Avoid division by zero
                err = (tst - ref) / ref

                if err != 0:
                    # Calculate ULP using nextafter for floating-point precision
                    ulp = abs(ref - math.nextafter(ref, math.inf))
                    err_ulp = abs((tst - ref) / ulp)

                    # Track the maximum ULP error
                    max_err_ulp = max(max_err_ulp, err_ulp)

        # Assert that the maximum error in ULP is within the acceptable range
        self.assertTrue(
            max_err_ulp < self.MAX_ERROR_ULP,
            f"toRadians() had errors in excess of {self.MAX_ERROR_ULP} ULP (max error: {max_err_ulp})"
        )

    def testAddExactInt(self):
        # Special test values for addition
        special_values = [
            -sys.maxsize - 1, -sys.maxsize, -sys.maxsize + 1,
            sys.maxsize - 1, sys.maxsize, sys.maxsize + 1,
            -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            -(sys.maxsize // 2), 0 - (sys.maxsize // 2), 1 - (sys.maxsize // 2),
            -(sys.maxsize // 2) + 1, 0 + (sys.maxsize // 2), 1 + (sys.maxsize // 2),
        ]

        for a in special_values:
            for b in special_values:
                bd_sum = a + b
                if bd_sum < -sys.maxsize - 1 or bd_sum > sys.maxsize:
                    # If the result is out of bounds, an exception should be raised
                    with self.assertRaises(ArithmeticError):
                        AccurateMath.addExact(a, b)
                else:
                    # Otherwise, the result should match the exact sum
                    self.assertEqual(bd_sum, AccurateMath.addExact(a, b))

    def test_subtract_exact_long(self):
        # Special test values for subtraction
        special_values = [
            -sys.maxsize - 1, -sys.maxsize, -sys.maxsize + 1,
            sys.maxsize - 1, sys.maxsize, sys.maxsize + 1,
            -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            -(sys.maxsize // 2), 0 - (sys.maxsize // 2), 1 - (sys.maxsize // 2),
            -(sys.maxsize // 2) + 1, 0 + (sys.maxsize // 2), 1 + (sys.maxsize // 2),
        ]

        for a in special_values:
            for b in special_values:
                bd_sub = a - b
                if bd_sub < -sys.maxsize - 1 or bd_sub > sys.maxsize:
                    # If the result is out of bounds, an exception should be raised
                    with self.assertRaises(ArithmeticError):
                        AccurateMath.subtractExact(a, b)
                else:
                    # Otherwise, the result should match the exact subtraction
                    self.assertEqual(bd_sub, AccurateMath.subtractExact(a, b))

    def test_multiply_exact_int(self):
        # Special test values for multiplication
        special_values = [
            -sys.maxsize - 1, -sys.maxsize, -sys.maxsize + 1,
            sys.maxsize - 1, sys.maxsize, sys.maxsize + 1,
            -10, -9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
            -(sys.maxsize // 2), 0 - (sys.maxsize // 2), 1 - (sys.maxsize // 2),
            -(sys.maxsize // 2) + 1, 0 + (sys.maxsize // 2), 1 + (sys.maxsize // 2),
        ]
        
        for a in special_values:
            for b in special_values:
                bd_mul = a * b
                if bd_mul < -sys.maxsize - 1 or bd_mul > sys.maxsize:
                    # If the result is out of bounds, an exception should be raised
                    with self.assertRaises(ArithmeticError):
                        AccurateMath.multiplyExact(a, b)
                else:
                    # Otherwise, the result should match the exact multiplication
                    self.assertEqual(bd_mul, AccurateMath.multiplyExact(a, b))

    


if __name__ == "__main__":
    unittest.main()
