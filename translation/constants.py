from openai import OpenAI
import os

#in your env if you don't have the OPENAI_API_KEY env variable, run in your terminal:
#`export OPENAI_API_KEY=XXXX_XXX_XX_XXX` where the XXXX_XXX_XX_XXX is a valid openai api key
CLIENT = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

SYSTEM_PROMPT = """
You are a coding assistant skilled in translating Java code into Python. Your main task is to take Java code as input and output Python code, ensuring class names remain the same. Please output only Python code, without '``` python' or '```' delimiters.

Guidelines for handling imports and dependencies:
1. All files will be in the same directory, so imports should be simple and direct without any package structure or relative import notation.
2. If one class (e.g., `TaskManager`) references another (e.g., `Task`), ensure the translated Python version of `TaskManager` includes a direct import, such as `import Task`.
3. Only include imports for classes that are actually referenced in the current file, and avoid using any relative imports (e.g., `from .task import Task`) or package-like imports (e.g., `from org.cornell import Task, from Task import Task`).

For translating test files:
1. Convert Java test annotations (e.g., `@Test`) into methods in a Python `unittest.TestCase` subclass.
2. Translate Java assertions like `assertEquals`, `assertTrue`, `assertFalse`, etc., to Python’s `unittest` methods (e.g., `assertEqual`, `assertTrue`).
3. Ensure that `import unittest` is included at the top of the test file to support testing functionality.
4. If required, you can import other Python modules as needed. If a class under test needs to be accessed as module-level variables, you can import it as a module.
5. Ensure that the test file is runnable, i.e, it contains a `if __name__ == '__main__':` block.
6. You may need to import other Python modules to run the test file, i.e, if TaskManager is used in the test file, you may need to import TaskManager as `from TaskManager import TaskManager`.
"""

FIND_ERROR_PROMPT = """
The following errors were manually detected when runnning tests on the code:
{formatted_errors}

These errors suggest that some methods, attributes, or class references may not have been correctly translated into Python. Please carefully review the following:
1. Ensure that all methods in the Java code are correctly translated into Python. Pay special attention to method names and signatures, making sure that method names from Java (e.g., `addTask`) are preserved exactly as they are in Python (i.e., `addTask`).
2. Check for any missing or incorrectly defined methods, properties, or class references. If a method or property is referenced in the Java code (e.g., `addTask`, `tasks.add()`, etc.) but is missing or incorrectly translated in Python, it must be properly implemented.
3. If the error involves an object or class, ensure that all necessary classes are imported and instantiated correctly in Python. Also, confirm that method calls on objects are using the correct attributes or methods as per the translated Python code.

If the errors are related to test files, remember the specific instructions for handling imports, dependencies, and test files mentioned earlier.

If there are any issues with missing methods, undefined attributes, or incorrect method references in the translated Python code, please correct them. When you fix these errors, output only the corrected Python code, without '``` python' or '```' delimiters.

Please remember the rules that were mentioned earlier about method and class translation.
"""

BASE_SETUP = [
    {"role": "system", "content": SYSTEM_PROMPT},
]

#OPTIONAL FOURTH LINE
# 4. If required, you can import other Python modules as needed. If a class under test needs to be accessed as module-level variables, you can import it as a module.
