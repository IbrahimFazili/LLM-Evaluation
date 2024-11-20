from openai import OpenAI
import os
import re
import subprocess

# CLIENT = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
SYSTEM_PROMPT = """
You are a coding assistant skilled in translating Java code into Python. Your main task is to take Java code as input and output Python code, ensuring class names remain the same. Please output only Python code, without '``` python' or '```' delimiters.

Guidelines for handling imports and dependencies:
1. All files will be in the same directory, so imports should be simple and direct without any package structure or relative import notation.
2. If one class (e.g., `TaskManager`) references another (e.g., `Task`), ensure the translated Python version of `TaskManager` includes a direct import, such as `import Task`.
3. Only include imports for classes that are actually referenced in the current file, and avoid using any relative imports (e.g., `from .task import Task`) or package-like imports (e.g., `from org.cornell import Task, from Task import Task`).
4. When translating the methods, **keep the method names exactly as they appear in Java** (e.g., `addTask` in Java should stay `addTask` in Python). Do not convert method names to snake_case (e.g., `addTask` should not become `add_task`).

For translating test files:
1. Convert Java test annotations (e.g., `@Test`) into methods in a Python `unittest.TestCase` subclass.
2. Translate Java assertions like `assertEquals`, `assertTrue`, `assertFalse`, etc., to Python’s `unittest` methods (e.g., `assertEqual`, `assertTrue`).
3. Ensure that `import unittest` is included at the top of the test file to support testing functionality.
4. If required, you can import other Python modules as needed. If a class under test needs to be accessed as module-level variables, you can import it as a module.

Following these instructions will produce Python code that maintains the original structure, dependencies, and test functionality of the Java code, with correct import statements.
"""

FIND_ERROR_PROMPT = """
The following errors were manually detected in the code:
{formatted_errors}

These errors suggest that some methods, attributes, or class references may not have been correctly translated into Python. Please carefully review the following:
1. Ensure that all methods in the Java code are correctly translated into Python. Pay special attention to method names and signatures, making sure that method names from Java (e.g., `addTask`) are preserved exactly as they are in Python (i.e., `addTask`).
2. Check for any missing or incorrectly defined methods, properties, or class references. If a method or property is referenced in the Java code (e.g., `addTask`, `tasks.add()`, etc.) but is missing or incorrectly translated in Python, it must be properly implemented.
3. If the error involves an object or class, ensure that all necessary classes are imported and instantiated correctly in Python. Also, confirm that method calls on objects are using the correct attributes or methods as per the translated Python code.

If there are any issues with missing methods, undefined attributes, or incorrect method references in the translated Python code, please correct them. When you fix these errors, output only the corrected Python code, without '``` python' or '```' delimiters.

Please remember the rules that were mentioned earlier about method and class translation.
"""

#in your env if you don't have the OPENAI_API_KEY env variable, run in your terminal:
#`export OPENAI_API_KEY=XXXX_XXX_XX_XXX` where the XXXX_XXX_XX_XXX is a valid openai api key

history = [
    {"role": "system", "content": SYSTEM_PROMPT},
]
def send_to_llm(input_string, system_prompt):
    # add it to the history
    history.append({"role": "user", "content": input_string})

    completion = CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=history
    )

    return completion

def gen_llm_output_java2python(input_path, output_path):
    try:
        # Open the file in read mode
        with open(input_path, 'r') as file:
            # Read the file content
            java_code = file.read()

        response = send_to_llm(java_code, SYSTEM_PROMPT)
        response_output = response.choices[0].message.content
        history.append({"role": "system", "content": response_output})

        # print(response_output)
        with open(output_path, 'w') as f:
            print(response_output, file=f)
    except Exception as e:
        print(f'Error reading file: {e}')

def detect_error_in_file(file_path):
    # use regex to find errors
    errors = []
    try:
        error_regex = r"^\[-\] Error: .+"

        # Read the contents of the file
        with open(file_path, 'r') as file:
            for line in file:
                if re.match(error_regex, line):
                    errors.append(line.strip())

        return errors
    except Exception as e:
        print(f'Error reading file: {e}')

def run_python_tests(test_script_path, result_file_path):
    """Run Python unit tests using pytest and save output to a file."""
    result = subprocess.run(
        ['pytest', test_script_path],
        capture_output=True, text=True
    )

    with open(result_file_path, 'w') as result_file:
        result_file.write("Standard Output:\n")
        result_file.write(result.stdout)
        result_file.write("\nStandard Error:\n")
        result_file.write(result.stderr)

    return result

# Main workflow

def main():
    # print('Translating files')

    # Translate Java files to Python
    # gen_llm_output_java2python('LLM-Evaluation/src/main/org/cornell/Task.java', 'ConvertedCode/Task.py')
    # gen_llm_output_java2python('LLM-Evaluation/src/main/org/cornell/TaskManager.java', 'ConvertedCode/TaskManager.py')
    # gen_llm_output_java2python('LLM-Evaluation/src/test/java/TaskManagerTest.java', 'ConvertedCode/TaskManagerTest.py')

    # Execute translated code with Java unit tests (before we retry)
    print('Executing translated code with Java unit tests...')
    execute_script_path = "./execute_java.sh"
    result = subprocess.run(execute_script_path, shell=True, capture_output=True, text=True)

    # Check for errors in the converted Java code
    errors = detect_error_in_file("ConvertedCode/converted.txt")
    #
    # # Retry translation if errors are found
    # while errors:
    #     print('Errors detected in translated code. Retrying...')
    #     formatted_errors = "\n".join([f"{i+1}. {error}" for i, error in enumerate(errors)])
    #     send_to_llm(FIND_ERROR_PROMPT.format(formatted_errors=formatted_errors), SYSTEM_PROMPT)
    #
    #     print('Retranslating files')
    #     gen_llm_output_java2python('LLM-Evaluation/src/main/org/cornell/Task.java', 'ConvertedCode/Task.py')
    #     gen_llm_output_java2python('LLM-Evaluation/src/main/org/cornell/TaskManager.java', 'ConvertedCode/TaskManager.py')
    #
    #     # Re-run the Java unit tests
    #     result = subprocess.run(execute_script_path, shell=True, capture_output=True, text=True)
    #
    #     # Check for any errors again
    #     errors = detect_error_in_file("ConvertedCode/converted.txt")
    #     print(f'Errors: {errors}')
    #
    # # After translation is fixed, run the Python unit tests
    # print('Executing translated code with Python unit tests...')
    # # @TODO implement workflow for test
    # test_script_path = "ConvertedCode/TaskManagerTest.py"
    # test_result_path = "ConvertedCode/testConvert.txt"
    # run_python_tests(test_script_path, test_result_path)

def isolate_python_error(file_path):
    #assuming error file is populated and formatted like test_error_output
    with open(file_path, 'r') as file:
        content = file.read()
    failure_pattern = re.compile(r"FAIL: .+")
    # Regex to match the traceback section
    traceback_pattern = re.compile(r"(Traceback \(most recent call last\):[\s\S]+?AssertionError: .+?)(?=\n\n|$)")

    # Find all failures
    failures = failure_pattern.findall(content)

    # Find all tracebacks associated with failures
    tracebacks = traceback_pattern.findall(content)

    # Combine failures with their corresponding tracebacks
    failure_info = []
    for i in range(len(failures)):
        failure_info.append({
            'failure': failures[i],
            'traceback': tracebacks[i] if i < len(tracebacks) else 'No traceback available'
        })

    return failure_info

print(isolate_python_error("test_error_output.txt"))



# main()