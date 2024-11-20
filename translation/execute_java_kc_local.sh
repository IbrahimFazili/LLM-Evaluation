#!/bin/bash

#remember to chmod this file!
# Path to the Java executable
#
#JAVA_PATH="/Users/ibrahimfazili/Library/Java/JavaVirtualMachines/temurin-17.0.10/Contents/Home/bin/java"
JAVA_PATH="/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home/bin/java"
# Output file path
#OUTPUT_PATH="/Users/ibrahimfazili/OneDrive - Cornell University/CS6158 Software Engineering in Machine Learning/LLM-Evaluation/ConvertedCode/converted.txt"
OUTPUT_PATH="/Users/kevincui/Desktop/LLM-Evaluation/ConvertedCode/converted.txt"
# Additional JVM options and classpath setup, with output redirected to the file
"$JAVA_PATH" -ea \
  -Didea.test.cyclic.buffer.size=1048576 \
  -javaagent:"/Applications/IntelliJ IDEA.app/Contents/lib/idea_rt.jar=55086:/Applications/IntelliJ IDEA.app/Contents/bin" \
  -Dfile.encoding=UTF-8 \
  -Dpolyglot.engine.WarnInterpreterOnly=false \
  -classpath "/Users/kevincui/.m2/repository/org/junit/platform/junit-platform-launcher/1.11.3/junit-platform-launcher-1.11.3.jar:/Applications/IntelliJ IDEA.app/Contents/lib/idea_rt.jar:/Applications/IntelliJ IDEA.app/Contents/plugins/junit/lib/junit5-rt.jar:/Applications/IntelliJ IDEA.app/Contents/plugins/junit/lib/junit-rt.jar:/Users/kevincui/Desktop/LLM-Evaluation/LLM-Evaluation/target/test-classes:/Users/kevincui/Desktop/LLM-Evaluation/LLM-Evaluation/target/classes:/Users/kevincui/.m2/repository/org/projectlombok/lombok/1.18.36/lombok-1.18.36.jar:/Users/kevincui/.m2/repository/org/junit/jupiter/junit-jupiter/5.11.3/junit-jupiter-5.11.3.jar:/Users/kevincui/.m2/repository/org/junit/jupiter/junit-jupiter-api/5.11.3/junit-jupiter-api-5.11.3.jar:/Users/kevincui/.m2/repository/org/opentest4j/opentest4j/1.3.0/opentest4j-1.3.0.jar:/Users/kevincui/.m2/repository/org/junit/platform/junit-platform-commons/1.11.3/junit-platform-commons-1.11.3.jar:/Users/kevincui/.m2/repository/org/apiguardian/apiguardian-api/1.1.2/apiguardian-api-1.1.2.jar:/Users/kevincui/.m2/repository/org/junit/jupiter/junit-jupiter-params/5.11.3/junit-jupiter-params-5.11.3.jar:/Users/kevincui/.m2/repository/org/junit/jupiter/junit-jupiter-engine/5.11.3/junit-jupiter-engine-5.11.3.jar:/Users/kevincui/.m2/repository/org/junit/platform/junit-platform-engine/1.11.3/junit-platform-engine-1.11.3.jar:/Users/kevincui/.m2/repository/org/graalvm/polyglot/polyglot/24.1.0/polyglot-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/sdk/collections/24.1.0/collections-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/sdk/nativeimage/24.1.0/nativeimage-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/sdk/word/24.1.0/word-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/python/python-language/24.1.0/python-language-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/truffle/truffle-api/24.1.0/truffle-api-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/tools/profiler-tool/24.1.0/profiler-tool-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/shadowed/json/24.1.0/json-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/regex/regex/24.1.0/regex-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/truffle/truffle-nfi/24.1.0/truffle-nfi-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/truffle/truffle-nfi-libffi/24.1.0/truffle-nfi-libffi-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/llvm/llvm-api/24.1.0/llvm-api-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/shadowed/icu4j/24.1.0/icu4j-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/shadowed/xz/24.1.0/xz-24.1.0.jar:/Users/kevincui/.m2/repository/org/bouncycastle/bcprov-jdk18on/1.76/bcprov-jdk18on-1.76.jar:/Users/kevincui/.m2/repository/org/bouncycastle/bcpkix-jdk18on/1.76/bcpkix-jdk18on-1.76.jar:/Users/kevincui/.m2/repository/org/bouncycastle/bcutil-jdk18on/1.76/bcutil-jdk18on-1.76.jar:/Users/kevincui/.m2/repository/org/graalvm/python/python-resources/24.1.0/python-resources-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/truffle/truffle-runtime/24.1.0/truffle-runtime-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/truffle/truffle-enterprise/24.1.0/truffle-enterprise-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/truffle/truffle-compiler/24.1.0/truffle-compiler-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/sdk/jniutils/24.1.0/jniutils-24.1.0.jar:/Users/kevincui/.m2/repository/org/graalvm/sdk/nativebridge/24.1.0/nativebridge-24.1.0.jar" \
  com.intellij.rt.junit.JUnitStarter -ideVersion5 -junit5 TaskManagerTestPython > "$OUTPUT_PATH"
#-classpath "/Users/ibrahimfazili/.m2/repository/org/junit/platform/junit-platform-launcher/1.11.3/junit-platform-launcher-1.11.3.jar:/Applications/IntelliJ IDEA CE.app/Contents/lib/idea_rt.jar:/Applications/IntelliJ IDEA CE.app/Contents/plugins/junit/lib/junit5-rt.jar:/Applications/IntelliJ IDEA CE.app/Contents/plugins/junit/lib/junit-rt.jar:/Users/ibrahimfazili/Library/CloudStorage/OneDrive-CornellUniversity/CS6158 Software Engineering in Machine Learning/LLM-Evaluation/LLM-Evaluation/target/test-classes:/Users/ibrahimfazili/Library/CloudStorage/OneDrive-CornellUniversity/CS6158 Software Engineering in Machine Learning/LLM-Evaluation/LLM-Evaluation/target/classes:/Users/ibrahimfazili/.m2/repository/org/projectlombok/lombok/1.18.34/lombok-1.18.34.jar:/Users/ibrahimfazili/.m2/repository/org/junit/jupiter/junit-jupiter/5.11.3/junit-jupiter-5.11.3.jar:/Users/ibrahimfazili/.m2/repository/org/junit/jupiter/junit-jupiter-api/5.11.3/junit-jupiter-api-5.11.3.jar:/Users/ibrahimfazili/.m2/repository/org/opentest4j/opentest4j/1.3.0/opentest4j-1.3.0.jar:/Users/ibrahimfazili/.m2/repository/org/junit/platform/junit-platform-commons/1.11.3/junit-platform-commons-1.11.3.jar:/Users/ibrahimfazili/.m2/repository/org/apiguardian/apiguardian-api/1.1.2/apiguardian-api-1.1.2.jar:/Users/ibrahimfazili/.m2/repository/org/junit/jupiter/junit-jupiter-params/5.11.3/junit-jupiter-params-5.11.3.jar:/Users/ibrahimfazili/.m2/repository/org/junit/jupiter/junit-jupiter-engine/5.11.3/junit-jupiter-engine-5.11.3.jar:/Users/ibrahimfazili/.m2/repository/org/junit/platform/junit-platform-engine/1.11.3/junit-platform-engine-1.11.3.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/polyglot/polyglot/24.1.0/polyglot-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/sdk/collections/24.1.0/collections-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/sdk/nativeimage/24.1.0/nativeimage-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/sdk/word/24.1.0/word-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/python/python-language/24.1.0/python-language-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/truffle/truffle-api/24.1.0/truffle-api-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/tools/profiler-tool/24.1.0/profiler-tool-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/shadowed/json/24.1.0/json-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/regex/regex/24.1.0/regex-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/truffle/truffle-nfi/24.1.0/truffle-nfi-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/truffle/truffle-nfi-libffi/24.1.0/truffle-nfi-libffi-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/llvm/llvm-api/24.1.0/llvm-api-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/shadowed/icu4j/24.1.0/icu4j-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/shadowed/xz/24.1.0/xz-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/bouncycastle/bcprov-jdk18on/1.76/bcprov-jdk18on-1.76.jar:/Users/ibrahimfazili/.m2/repository/org/bouncycastle/bcpkix-jdk18on/1.76/bcpkix-jdk18on-1.76.jar:/Users/ibrahimfazili/.m2/repository/org/bouncycastle/bcutil-jdk18on/1.76/bcutil-jdk18on-1.76.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/python/python-resources/24.1.0/python-resources-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/truffle/truffle-runtime/24.1.0/truffle-runtime-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/truffle/truffle-enterprise/24.1.0/truffle-enterprise-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/truffle/truffle-compiler/24.1.0/truffle-compiler-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/sdk/jniutils/24.1.0/jniutils-24.1.0.jar:/Users/ibrahimfazili/.m2/repository/org/graalvm/sdk/nativebridge/24.1.0/nativebridge-24.1.0.jar" \