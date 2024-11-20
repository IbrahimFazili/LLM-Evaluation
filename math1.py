class Math:
    PRECISION = 1e-4

    @staticmethod
    def abs(a):
        if a < 0:
            return -a
        return a

    @staticmethod
    def pow(base, exponent):
        res = 1
        while exponent > 0:
            res *= base
            exponent -= 1
        return res

    @staticmethod
    def max(a, b):
        if a > b:
            return a
        return b

    @staticmethod
    def min(a, b):
        if a < b:
            return a
        return b

    @staticmethod
    def naturallog(num):
        accuracy = 1000
        sum = 0
        for n in range(accuracy):
            num1 = (1.0 / (2 * n + 1))
            num2 = (num - 1) / (num + 1)

            sum += num1 * Math.pow(num2, 2 * n + 1)
        return 2 * sum

    @staticmethod
    def ceil(x):
        intPart = int(x)

        if x == intPart:
            return intPart
        else:
            return intPart + 1

    @staticmethod
    def squareroot(num):
        lo = Math.min(1, num)
        hi = Math.max(1, num)
        mid = 0

        while 100 * lo * lo < num:
            lo *= 10
        while 0.01 * hi * hi > num:
            hi *= 0.1

        for i in range(100):
            mid = (lo + hi) / 2
            if mid * mid == num:
                return mid
            if mid * mid > num:
                hi = mid
            else:
                lo = mid
        return mid

    @staticmethod
    def factorial(n):
        result = 1
        for i in range(2, int(n) + 1):
            result *= i
        return result

    @staticmethod
    def toRadians(degrees):
        return degrees * 3.141592653589793 / 180

    @staticmethod
    def toDegrees(radians):
        return radians * 180 / 3.141592653589793

