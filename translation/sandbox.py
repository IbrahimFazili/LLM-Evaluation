from constants import *
import os, datetime
import subprocess
import re


def send_to_llm(input_prompt, temp=None, history=None):
    # add it to the history
    if not history:
        #general purpose AI, no system prompting
        history = []
    history.append({"role": "user", "content": input_prompt})

    if temp:
        completion = CLIENT.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
            temperature=temp,
        )
    else:
        completion = CLIENT.chat.completions.create(
            model="gpt-4o-mini",
            messages=history,
        )
    return completion

def gen_llm_output_java2python(input_path, output_path, temp=None, history=BASE_SETUP, feedback=False):
    # now we're assuming that we are generating code so history = BASE_SETUP

    if not feedback:
        try:
            # Open the file in read mode
            with open(input_path, 'r') as file:
                # Read the file content
                java_code = file.read()

            response = send_to_llm(java_code, temp=temp, history=history)
            response_output = response.choices[0].message.content
            with open(output_path, 'w') as f:
                print(response_output, file=f)
        except Exception as e:
            print(f'Error reading file: {e}')

def save_outputs(files, input_dir, output_dir):
    for file in files:
        gen_llm_output_java2python(input_dir + file + '.java', output_dir + "/" + file + '.py', temp=0)
        print(f'Generated file: {file}')

def detect_error_in_file(file_path):
    # use regex to find errors
    errors = []
    try:
        with open(file_path, 'r') as file:
            line_no = 0
            for line in file:
                line_no += 1
                # print(line)
                match = re.search(r"(?<=message=').*(?=' details=')", line)
                if match:
                    # print(line_no)
                    errors.append(match.group())

        return errors
    except Exception as e:
        print(f'Error reading file: {e}')

def feedback_loop():
    pass

if __name__ == "__main__":
    #do stuff
    # response = send_to_llm("Tell me a story about dogs in 100 words or less.", temp=0)
    # print(response.choices[0].message.content)

    # files = ["Math", "Task", "TaskManager"]
    # input_dir = 'LLM-Evaluation/src/main/org/cornell/'
    # output_dir = os.path.join(os.getcwd(), 'translation/', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    # os.makedirs(output_dir)
    # save_outputs(files, input_dir, output_dir)
    #make sure to make files readable in this directory
    # execute_script_path = "translation/execute_java_kc_local.sh"
    # result = subprocess.run(execute_script_path, shell=True, capture_output=True, text=True)
    # print(os.getcwd())
    errors = detect_error_in_file("ConvertedCode/converted.txt")
    print(errors)

# main()

#
# def run_python_tests(test_script_path, result_file_path):
#     """Run Python unit tests using pytest and save output to a file."""
#     result = subprocess.run(
#         ['pytest', test_script_path],
#         capture_output=True, text=True
#     )
#
#     with open(result_file_path, 'w') as result_file:
#         result_file.write("Standard Output:\n")
#         result_file.write(result.stdout)
#         result_file.write("\nStandard Error:\n")
#         result_file.write(result.stderr)
#
#     return result

# Main workflow

# def main():
#     print('Translating files')
#
#     # Translate Java files to Python
#     gen_llm_output_java2python('LLM-Evaluation/src/main/org/cornell/Task.java', 'ConvertedCode/Task.py')
#     gen_llm_output_java2python('LLM-Evaluation/src/main/org/cornell/TaskManager.java', 'ConvertedCode/TaskManager.py')
#     gen_llm_output_java2python('LLM-Evaluation/src/test/java/TaskManagerTest.java', 'ConvertedCode/TaskManagerTest.py')
#
#     # Execute translated code with Java unit tests (before we retry)
#     print('Executing translated code with Java unit tests...')
#     execute_script_path = "./execute_java.sh"
#     result = subprocess.run(execute_script_path, shell=True, capture_output=True, text=True)
#
#     # Check for errors in the converted Java code
#     errors = detect_error_in_file("ConvertedCode/converted.txt")
#
#     # Retry translation if errors are found
#     while errors:
#         print('Errors detected in translated code. Retrying...')
#         formatted_errors = "\n".join([f"{i+1}. {error}" for i, error in enumerate(errors)])
#         send_to_llm(FIND_ERROR_PROMPT.format(formatted_errors=formatted_errors), SYSTEM_PROMPT)
#
#         print('Retranslating files')
#         gen_llm_output_java2python('LLM-Evaluation/src/main/org/cornell/Task.java', 'ConvertedCode/Task.py')
#         gen_llm_output_java2python('LLM-Evaluation/src/main/org/cornell/TaskManager.java', 'ConvertedCode/TaskManager.py')
#
#         # Re-run the Java unit tests
#         result = subprocess.run(execute_script_path, shell=True, capture_output=True, text=True)
#
#         # Check for any errors again
#         errors = detect_error_in_file("ConvertedCode/converted.txt")
#         print(f'Errors: {errors}')
#
#     # After translation is fixed, run the Python unit tests
#     print('Executing translated code with Python unit tests...')
#     # @TODO implement workflow for test
#     test_script_path = "ConvertedCode/TaskManagerTest.py"
#     test_result_path = "ConvertedCode/testConvert.txt"
#     run_python_tests(test_script_path, test_result_path)