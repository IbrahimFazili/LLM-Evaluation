from constants import *
import os, datetime
import subprocess
import re
import shutil


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
    history.append({"role": "assistant", "content": completion.choices[0].message.content})
    return completion

def gen_llm_output_java2python(input_path, output_path, isPhase2, temp=None, history=BASE_SETUP, feedback=False):
    # now we're assuming that we are generating code so history = BASE_SETUP
    hist = history.copy()
    if not feedback:
        try:
            # Open the file in read mode
            with open(input_path, 'r') as file:
                # Read the file content
                java_code = file.read()

            response = send_to_llm(java_code, temp=temp, history=hist)
            response_output = response.choices[0].message.content
            with open(output_path, 'w') as f:
                print(response_output, file=f)
        except Exception as e:
            print(f'Error reading file: {e}')
    else:
        try:
            # Open the file in read mode
            if not isPhase2:
                errors = detect_error_in_file(input_path)
            else:
                errors = detect_errors_in_test_output(input_path)
            if errors:
                formatted_errors = "\n".join([f"{i+1}. {error}" for i, error in enumerate(errors)])

                response = send_to_llm(FIND_ERROR_PROMPT.format(formatted_errors=formatted_errors), temp=temp, history=hist)
                response_output = response.choices[0].message.content
                with open(output_path, 'w') as f:
                    print(response_output, file=f)

            #if no errors don't do anything
        except Exception as e:
            print(f'Error reading file: {e}')


    # we affect history in send_to_llm in response, so we can return it in case of use in feedback loop
    return hist

def feedback_loop(error_path, files, response_history, output_dir, isPhase2):
    for file in files:
        response_history[file] = gen_llm_output_java2python(error_path, output_dir + "/" + file + ".py", isPhase2, temp = 0.2, history=response_history[file], feedback=True)
        shutil.copyfile(output_dir + "/" + file + '.py', 'temp/' + file + '.py')
    return response_history


def save_outputs(files, input_dir, output_dir, isPhase2, response_history=None):
    #we want to keep a tally of the histories for each of the responses
    if not response_history:
        response_history = {}
    for file in files:
        response_history[file] = gen_llm_output_java2python(input_dir + file + '.java', output_dir + "/" + file + '.py', isPhase2=isPhase2, temp=0.2)
        shutil.copyfile(output_dir + "/" + file + '.py', 'temp/' + file + '.py')
        print(f'Generated file: {file}')
    return response_history

def detect_errors_in_test_output(test_output):
    """Function to detect errors in the test output using regular expressions."""
    errors = []

    try:
        with open(test_output, 'r') as file:
            test_output_content = file.read()
            # Ignore the "short test summary info" section by removing it from the content
            summary_start = re.search(r"=+ short test summary info =+", test_output_content)
            if summary_start:
                test_output_content = test_output_content[:summary_start.start()]

            # Regular expressions to match different error patterns in the test output
            error_patterns = [
                # Match error trace with test method, error type, error message, and failing line
                r"(?P<test_name>[\w\.]+)\s+.*?E\s+(?P<error_type>\w+):\s+(?P<error_msg>[^\n]+)\n.*?\n(?P<failing_line>.*?):(?P<line_number>\d+): (?P<error_type_duplicate>\w+)",
            ]

            # Iterate over the error patterns
            for pattern in error_patterns:
                matches = re.finditer(pattern, test_output_content, re.DOTALL)
                for match in matches:
                    # Collect the match details into a formatted string
                    error_detail = (
                        f"Test '{match.group('test_name')}' failed with {match.group('error_type')}: "
                        f"{match.group('error_msg')} (at {match.group('failing_line')}:{match.group('line_number')})"
                    )
                    errors.append(error_detail)

            return errors
    except Exception as e:
        print(f'Error reading file: {e}')

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

def check_translation(execute_script_path, output_dir, run_no, response_history, error_path):
    #mutator function that simply abstracts out some of the code
    with open(output_dir+f'/run_{run_no}/'+"response_history.txt", 'w') as f:
        print(response_history, file=f)
    #
    print("Checking answers")
    subprocess.run(execute_script_path, shell=True, capture_output=True, text=True)
    errors = detect_error_in_file(error_path)
    shutil.copyfile(error_path, output_dir+f'/run_{run_no}/'+"error_output.txt")
    return errors

def check_test(test_files, output_dir, run_no, response_history, error_path):
    """
    Runs the Python test files, saves the response to a text file, and counts errors.
    """
    # Save the response history to a text file
    with open(output_dir+f'/test_run_{run_no}/'+"response_history.txt", 'w') as f:
        print(response_history, file=f)

    errors_collected = []  # Collect errors for all test files

    for test_file_name in test_files:
        test_file_path = os.path.join('temp', f'{test_file_name}.py')

        # Run the Python test file using subprocess
        try:
            # Open the error_path to write combined stdout and stderr
            with open(error_path, 'w') as error_file:
                result = subprocess.run(
                    ['pytest', test_file_path],  # Using pytest to run the test
                    stdout=subprocess.PIPE,      # Capture stdout in result
                    stderr=subprocess.STDOUT,    # Merge stderr with stdout
                    text=True,                   # Return output as text (not bytes)
                    check=False                  # Don't raise an exception on non-zero exit status
                )

                # Write the combined output to the error file
                error_file.write(result.stdout)

            # Check for errors in the output
            errors = detect_errors_in_test_output(error_path)

            # Save the test result to the output folder
            test_output_path = os.path.join(output_dir, f'test_run_{run_no}', f"{test_file_name}_test_output.txt")
            with open(test_output_path, 'w') as f:
                f.write(result.stdout)

            # Optionally save the error messages to a separate file
            if errors:
                error_output_path = os.path.join(output_dir, f'test_run_{run_no}', f"{test_file_name}_error_output.txt")
                with open(error_output_path, 'w') as f:
                    f.write("\n".join(errors))

            # Accumulate errors
            errors_collected.extend(errors)

        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running the test: {e}")
            errors_collected.append(f"Test failed for {test_file_name}: {e}")

    # After all tests are run, return the accumulated errors
    if errors_collected:
        return errors_collected
    else:
        return []  # No errors

def llm_translate(files, input_dir, output_dir, execute_script_path, error_path, testFiles, input_dir_test, num_of_retries=5):
    os.makedirs(output_dir)
    run_no = 1
    os.makedirs(output_dir + f'/run_{run_no}/')
    print("**** STARTING PHASE 1 ****")
    response_history = save_outputs(files, input_dir, output_dir+f'/run_{run_no}/', isPhase2=False)
    if num_of_retries > 0:
        errors = check_translation(execute_script_path, output_dir, run_no, response_history, error_path)
        if errors:
            print("Errors detected in translated source code, initiating step 1a (feedback loop)")
        while errors:
            # print("ENTERING FEEDBACK LOOP")
            if run_no == num_of_retries:
                break
            run_no += 1
            print(f'Number of errors detected: {len(errors)}')
            print(f'Source code loop {run_no-1}')
            os.makedirs(output_dir + f'/run_{run_no}')
            response_history = feedback_loop(error_path, files, response_history, output_dir+f'/run_{run_no}', False)
            errors = check_translation(execute_script_path, output_dir, run_no, response_history, error_path)

        if not errors:
            print(f'Source code successfully translated after {run_no-1} feedback iterations.')
        else:
            print(f'Max iteration count reached. Number of remaining errors in source code: {len(errors)}')
            # print("WOMP WOMP :(")
    else:
        pass
        # print("NOT ENTERING FEEDBACK LOOP")


    #PHASE 2
    print("\n")
    print("**** PHASE 1 COMPLETE, STARTING PHASE 2 ****")
    test_run_no = 1
    os.makedirs(output_dir + f'/test_run_{test_run_no}')
    response_history = save_outputs(testFiles, input_dir_test, output_dir+f'/test_run_{test_run_no}',True, response_history)
    if num_of_retries > 0:
        errors = check_test(testFiles, output_dir, test_run_no, response_history, error_path)
        if errors:
            print("Errors detected in translated test files, initiating step 2a (feedback loop)")
        while errors:
            if test_run_no == num_of_retries:
                break
            test_run_no += 1
            print(f'Number of errors detected: {len(errors)}')
            print(f'Test code loop {test_run_no-1}')
            os.makedirs(output_dir + f'/test_run_{test_run_no}')
            response_history = feedback_loop(error_path, testFiles, response_history, output_dir+f'/test_run_{test_run_no}', True)
            errors = check_test(testFiles, output_dir, test_run_no, response_history, error_path)

        if not errors:
            print(f'Test code successfully translated after {test_run_no-1} feedback iterations.')
        else:
            print(f'Max iteration count reached. Number of remaining errors in source code: {len(errors)}')
            # print("WOMP WOMP :(")
    else:
        pass

    print("**** PHASE 2 COMPLETE****")
    print(f'Results saved in {output_dir}')

    return response_history
if __name__ == "__main__":
    #files should only correspond to the files within a given package

    # files = ["Task", "TaskManager"]
    files = ['AccurateMath', "AccurateMathCalc", "AccurateMathLiteralArrays"]
    # input_dir = 'LLM-Evaluation/src/main/org/cornell/'
    input_dir = 'commons-math/commons-math-core/src/main/java/org/apache/commons/math4/core/jdkmath/'
    output_dir = os.path.join(os.getcwd(), 'translation/', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    execute_script_path = "translation/execute_java_kc_local.sh"
    error_path = "ConvertedCode/converted.txt"
    testFiles = "AccurateMathStrictComparisonTest"
    # testFiles = ["TaskManagerTest"]
    # input_dir_test = 'LLM-Evaluation/src/test/java/'
    input_dir_test = "commons-math/commons-math-legacy-core/src/test/java/org/apache/commons/math4/legacy/core/jdkmath/"

    llm_translate(files, input_dir, output_dir, execute_script_path, error_path, testFiles, input_dir_test)


