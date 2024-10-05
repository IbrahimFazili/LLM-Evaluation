import math

class Math:

    PRECISION = 1e-4

    @staticmethod
    def abs(number):
        if number < 0:
            return -number
        else:
            return number
        

    @staticmethod
    def pow(base, exponent):
        if exponent == 0:
            return 1
        return base**exponent
    
    @staticmethod
    def max(a, b):
        if a > b:
            return a
        else:
            return b
        
    @staticmethod
    def min(a, b):
        if a < b:
            return a
        else:
            return b
        
    @staticmethod
    def naturallog(number):
        # source https://stackoverflow.com/questions/13211137/get-logarithm-without-math-log-python
        n = 1000000.0 # for precision
        return n * ((number ** (1/n)) - 1)
    

    @staticmethod
    def ceil(number):
        intPart = int(number)
        if intPart == number:
            return intPart
        else:
            return intPart + 1
        
    @staticmethod
    def squareroot(number):
        return number**0.5
    
    @staticmethod
    def factorial(n):
        result = 1

        for i in range(2, n+1):
            result *= i
        
        return result
    
    @staticmethod 
    def toRadians(degrees):
        return degrees * (math.pi / 180)
    
    @staticmethod
    def toDegrees(radians):
        return radians * (180 / math.pi)
