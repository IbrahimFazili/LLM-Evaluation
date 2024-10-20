import org.junit.jupiter.api.Test;

import static org.cornell.Math.*;

public class MathTest {
    @Test
    public void test1() {
        double base = 10;
        double exponent = 2;

        double result = pow(base, exponent);
        assert result == 100;

        result *= 0.5;
        result += 14;
        result = squareroot(result);
        assert result == 8;

        double f = factorial(4);

        assert min(f, result) == result;
    }

    @Test
    public void test2() {
        double degree = 34;
        double radian = 0.593412;

        double radianTest = toRadians(degree);
        double degreeTest = toDegrees(radian);

        assert abs(radianTest - radian) <= PRECISION;
        assert abs(degree - degreeTest) <= PRECISION;
    }

    @Test
    public void test3() {
        double number = 5;
        double nlog = naturallog(number);
        assert abs(nlog - Math.log(number)) <= PRECISION;

        double ceiling = ceil(nlog);
        assert ceiling == 2;

        double p = pow(ceiling, ceiling);
        assert p == 4;

        assert min(number, p) == p;
        double f = factorial(5 * 2);
        double sqrt = squareroot(f);

        assert abs(sqrt - Math.sqrt(f)) <= PRECISION;

        p += (double) 24 / 5;
        assert abs(toRadians(p) - Math.toRadians(p)) <= PRECISION;
    }
}