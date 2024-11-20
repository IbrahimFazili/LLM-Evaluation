import org.junit.jupiter.api.Test;

import org.graalvm.polyglot.Context;
import org.graalvm.polyglot.Value;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class MathTestPython {
    private String pythonScript;

    public MathTestPython() throws IOException {
        //adjust the path as needed
        Path parentPath = Paths.get("").toAbsolutePath().getParent();
        pythonScript = new String(
                Files.readAllBytes(Paths.get(parentPath + "/translation/test_results/Math.py")));
    }

    @Test
    void test1() {

        try (Context context = Context.newBuilder().allowAllAccess(true).build()) {
            // Evaluate the Python file content
            context.eval("python", pythonScript);

            // Call the Python functions
            Value mathClass = context.getBindings("python").getMember("Math");

            // Access static methods from the Math class
            Value powFunction = mathClass.getMember("pow");
            Value squareRootFunction = mathClass.getMember("squareroot");
            Value factorialFunction = mathClass.getMember("factorial");
            Value minFunction = mathClass.getMember("min");

            double base = 10;
            double exponent = 2;

            double result = powFunction.execute(base, exponent).asDouble();
            assert result == 100;

            result *= 0.5;
            result += 14;
            result = squareRootFunction.execute(result).asDouble();
            assert result == 8;

            double f = factorialFunction.execute((int) result).asDouble();

            assert minFunction.execute(f, result).asDouble() == result;
        }
    }

    @Test
    void test2() {

        try (Context context = Context.newBuilder().allowAllAccess(true).build()) {
            context.eval("python", pythonScript);

            // Call the Python functions
            Value mathClass = context.getBindings("python").getMember("Math");

            Value toDegreesFunction = mathClass.getMember("toDegrees");
            Value toRadiansFunction = mathClass.getMember("toRadians");
            Value precisionValue = mathClass.getMember("PRECISION");
            Value absFunction = mathClass.getMember("abs");

            double degree = 34;
            double radian = 0.593412;

            double radianTest = toRadiansFunction.execute(degree).asDouble();
            double degreeTest = toDegreesFunction.execute(radian).asDouble();

            assert absFunction.execute(radianTest - radian).asDouble() <= precisionValue.asDouble();
            assert absFunction.execute(degree - degreeTest).asDouble() <= precisionValue.asDouble();
        }
    }

    @Test
    void test3() {
        try (Context context = Context.newBuilder().allowAllAccess(true).build()) {
            context.eval("python", pythonScript);

            // Call the Python functions
            Value mathClass = context.getBindings("python").getMember("Math");

            Value naturallogFunction = mathClass.getMember("naturallog");
            Value ceilFunction = mathClass.getMember("ceil");
            Value powFunction = mathClass.getMember("pow");
            Value minFunction = mathClass.getMember("min");
            Value squarerootFunction = mathClass.getMember("squareroot");
            Value factorialFunction = mathClass.getMember("factorial");
            Value toRadiansFunction = mathClass.getMember("toRadians");
            Value precisionValue = mathClass.getMember("PRECISION");
            Value absFunction = mathClass.getMember("abs");

            double number = 5;
            double nlog = naturallogFunction.execute(number).asDouble();

            assert absFunction.execute(nlog - Math.log(number)).asDouble() <= precisionValue.asDouble();

            double ceiling = ceilFunction.execute(nlog).asDouble();
            assert ceiling == 2;

            double p = powFunction.execute(ceiling, ceiling).asDouble();
            assert p == 4;

            assert minFunction.execute(number, p).asDouble() == p;
            double f = factorialFunction.execute(5*2).asDouble();
            double sqrt = squarerootFunction.execute(f).asDouble();

            assert absFunction.execute(sqrt - Math.sqrt(f)).asDouble() <= precisionValue.asDouble();

            p += (double) 24 / 5;

            assert absFunction.execute(toRadiansFunction.execute(p).asDouble() - Math.toRadians(p)).asDouble() <= precisionValue.asDouble();
        }
    }
}
