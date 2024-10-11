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
        # source https://www.reddit.com/r/javahelp/comments/ybbu3k/can_we_find_natural_log_without_mathlog/
        # example of code which is hard to translate
        e = 2.718281828459045
        epsilon=1e-10
        low, high = 0, number
        if number < 1:
            high = 1

        # Perform binary search
        while high - low > epsilon:
            mid = (low + high) / 2
            exp_mid = e ** mid  # Calculate exp(mid)

            # Adjust the bounds based on the comparison
            if exp_mid < number:
                low = mid  # Move the lower bound up
            else:
                high = mid  # Move the upper bound down

        return (low + high) / 2
    

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
