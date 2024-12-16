package cornell;

import static java.lang.Math.PI;

public class MathHandwritten {

    public static double PRECISION = 1e-4;

    public static double abs(double a) {
        if (a < 0) {
            return -a;
        }
        return a;
    }

    public static double pow(double base, double exponent) {
        double res = 1;
        while (exponent > 0) {
            res *= base;
            exponent -= 1;
        }
        return res;
    }

    public static double max(double a, double b) {
        if (a > b) {
            return a;
        }
        return b;
    }

    public static double min(double a, double b) {
        if (a < b) {
            return a;
        }
        return b;
    }

    public static double naturallog(double num) {
        // source code from
        // https://stackoverflow.com/questions/59270651/mathematical-operations-without-using-java-math-class
        int accuracy = 1000;
        double sum = 0;
        for(int n = 0; n < accuracy; n++) {
            double num1 = (1.0/(2*n+1));
            double num2 = (num-1)/(num+1);

            sum += num1*pow(num2,2*n+1);
        }
        return 2 * sum;
    }

    public static int ceil(double x) {
        int intPart = (int) x;

        if (x == intPart) {
            return intPart;
        } else {
            return intPart + 1;
        }
    }

    public static double squareroot(double num) {
        // source code https://stackoverflow.com/questions/3581528/how-is-the-square-root-function-implemented
        double lo = min(1, num), hi = max(1, num), mid = 0;

        // Update the bounds to be off the target by a factor of 10
        while(100 * lo * lo < num) lo *= 10;
        while(0.01 * hi * hi > num) hi *= 0.1;

        for(int i = 0 ; i < 100 ; i++){
            mid = (lo+hi)/2;
            if(mid*mid == num) return mid;
            if(mid*mid > num) hi = mid;
            else lo = mid;
        }
        return mid;
    }

    public static double factorial(double n) {
        int result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    public static double toRadians(double degrees) {
        return degrees * PI / 180;
    }

    public static double toDegrees(double radians) {
        return radians * 180 / PI;
    }
}