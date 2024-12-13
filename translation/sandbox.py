
# here we will test python to python code
from translate import *
import os
import datetime
import subprocess


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

if __name__ == "__main__":
    files = ["TaskManagerTest"]
    input_dir = 'LLM-Evaluation/src/test/java/'
    output_dir = os.path.join(os.getcwd(), 'translation/', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    execute_script_path = "translation/execute_java_kc_local.sh" #TODO: CHANGE
    error_path = "ConvertedCode/pytest_output2.txt" #TODO: CHANGE
    #
    # llm_translate(files, input_dir, output_dir, execute_script_path, error_path, num_of_retries=0)
    for file in files:
        run_python_tests(f'temp/{file}.py', error_path)
        #we're gonna need a feedback loop here too
        # run_python_tests('ConvertedCode/TaskManagerTest.py', error_path)