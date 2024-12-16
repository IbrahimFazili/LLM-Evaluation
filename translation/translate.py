from constants import *
from utils import *
import os, datetime
import subprocess
import re
import shutil
import argparse

#p1
def source_code_translate(files, input_dir, output_dir, execute_script_path, error_path, num_of_retries, temp):
    run_no = 1
    os.makedirs(output_dir + f'/run_{run_no}/')
    response_history = save_outputs(files, input_dir, output_dir+f'/run_{run_no}/', isPhase2=False, temp=temp)
    if num_of_retries > 0:
        errors = check_translation(execute_script_path, output_dir, run_no, response_history, error_path)
        if errors:
            print("Errors detected in translated source code, initiating step 1a (feedback loop)")
        while errors:
            if run_no == num_of_retries:
                break
            run_no += 1
            print(f'Number of errors detected: {len(errors)}')
            print(f'Source code loop {run_no-1}')
            os.makedirs(output_dir + f'/run_{run_no}')
            response_history = feedback_loop(error_path, files, response_history, output_dir+f'/run_{run_no}', False, temp)
            errors = check_translation(execute_script_path, output_dir, run_no, response_history, error_path)

        if not errors:
            print(f'Source code successfully translated after {run_no-1} feedback iterations.')
        else:
            print(f'Max iteration count reached. Number of remaining errors in source code: {len(errors)}')
    return response_history, errors, run_no

#p2
def source_test_translate(output_dir, error_path, testFiles, input_dir_test, history, files, run_no, num_of_retries, temp):
    test_run_no = 1
    os.makedirs(output_dir + f'/test_run_{test_run_no}')
    response_history = save_outputs(testFiles, input_dir_test, output_dir+f'/test_run_{test_run_no}',True, history, temp=temp)
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
            response_history = feedback_loop(error_path, testFiles, response_history, output_dir+f'/test_run_{test_run_no}', True, temp)
            errors = check_test(testFiles, output_dir, test_run_no, response_history, error_path)

            #phase 2b
            if not errors:
                print("Initiating phase 2b: Mutation Testing")
                mutation_test_errors = mutation_test(files, testFiles, output_dir, run_no, test_run_no, error_path)
    #             if not passing_mutation_test:
                if not mutation_test_errors:
                    break
                else:
                    errors = mutation_test_errors
        if not errors:
            print(f'Test code successfully translated after {test_run_no-1} feedback iterations.')
        else:
            print(f'Max iteration count reached. Number of remaining errors in source code: {len(errors)}')
            # print("WOMP WOMP :(")
    return response_history

#p2b
def mutation_test(files, testFiles, output_dir, run_no, test_run_no, error_path):
    #first copy all necessary files into temp
    for testFile in testFiles:
        shutil.copyfile(output_dir + f'/test_run_{test_run_no}/' + testFile + '.py', 'temp/' + testFile + '.py')
    num_fn_iterations = 0
    for i in range(1,run_no):
        for file in files:
            shutil.copyfile(output_dir + f'/run_{i}/' + file + '.py', 'temp/' + file + '.py')

        #running mutation testing (should fail at least once for each)
        num_fp_files = 0
        return_errors = []
        for test_file_name in testFiles:
            test_file_path = os.path.join('temp/', f'{test_file_name}.py')
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
                    error_file.write(result.stdout)

                errors = detect_errors_in_test_output(error_path)
                if not errors:
                    print(f'Mutation test failed (actual test passed) for {test_file_name} in run_no: {i}')
                    return_errors.append(f'Mutation test failed (actual test passed) for {test_file_name} in run_no: {i}')
                if errors:
                    num_fp_files += 1
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while running the test: {e}")

        # After all tests are run, return the accumulated errors
        if num_fp_files == 0: #BAD
            print(f'Mutation testing passed for run_no: {i}. Tests are not strong enough.')
            num_fn_iterations += 1
        num_fp_files = 0
    if num_fn_iterations == 0: #GOOD!
        print(f'Mutation testing succeeded for all runs from run numbers 1 to {run_no}.')
    return return_errors


def llm_translate(files, input_dir, output_dir, execute_script_path, error_path, testFiles, input_dir_test, testing_phase_2=True, num_of_retries=DEFAULT_NUM_RETRIES, temp = 0.2):
    print("**** STARTING PHASE 1: Source Code Translation ****")
    os.makedirs(output_dir)
    response_history, errors, run_no = source_code_translate(files, input_dir, output_dir, execute_script_path, error_path, num_of_retries, temp)
    print("**** PHASE 1 COMPLETE ****")
    print("\n")
    print("**** STARTING PHASE 2: Source Test Translation ****")
    #if there are errors, we should only run the test generation once because the source code had issues
    if errors:
        num_of_retries = 0
    response_history = source_test_translate(output_dir, error_path, testFiles, input_dir_test, response_history, files, run_no, num_of_retries, temp)
    print("**** PHASE 2 COMPLETE ****")
    print("\n")
    print(f'Results saved in {output_dir}')

    return response_history


def mixed_modality_translate(files, input_dir, output_dir, error_path, testFiles, input_dir_test, num_of_retries=DEFAULT_NUM_RETRIES, temp = 0.2):
    #called on sandbox = 1
    #a mix of phase 1 and phase 2
    #testing translated source code on ground truth proven translated tests
    os.makedirs(output_dir)
    print("**** STARTING MIXED MODALITY TRANSLATION ****")
    run_no = 1
    os.makedirs(output_dir + f'/test_run_{run_no}/')
    response_history = save_outputs(files, input_dir, output_dir+f'/test_run_{run_no}/', isPhase2=False, temp = temp)
    if num_of_retries > 0:
        for testFile in testFiles:
            shutil.copyfile(input_dir_test + "/" + testFile + '.py', 'temp/' + testFile + '.py')
        errors = check_test(testFiles, output_dir, run_no, response_history, error_path)
        if errors:
            print("Errors detected in translated source files. Triggering feedback loop: ")
        while errors:
            if run_no == num_of_retries:
                break
            run_no += 1
            print(f'Number of errors detected: {len(errors)}')
            print(f'Feedback loop {run_no-1}')
            os.makedirs(output_dir + f'/test_run_{run_no}')
            response_history = feedback_loop(error_path, files, response_history, output_dir+f'/test_run_{run_no}', True, temp)
            errors = check_test(testFiles, output_dir, run_no, response_history, error_path)

        if not errors:
            print(f'Code successfully translated after {run_no-1} feedback iterations.')
        else:
            print(f'Max iteration count reached. Number of remaining errors in source code: {len(errors)}')
    print("MIXED MODALITY TRANSLATION COMPLETE")
    print(f'Results saved in {output_dir}')
    return response_history

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run LLM translation script with specified parameters.")

    parser.add_argument('--files', nargs='+', required=True, help='List of files within a given package')
    parser.add_argument('--input_dir', required=True, help='Input directory path')
    parser.add_argument('--output_dir', help='Output directory path') #not required
    parser.add_argument('--execute_script_path', help='Path to the execute script') #not required
    parser.add_argument('--test_files', nargs='+', required=True, help='List of test files')
    parser.add_argument('--input_dir_test', required=True, help='Input directory path for test files')
    parser.add_argument('--temperature', help='Input temperature for code generation')
    parser.add_argument('--sandbox', help='Sandbox codes for running parts of the translation process independently')

    args = parser.parse_args()
#
    if args.output_dir is None:
        args.output_dir = os.path.join(os.getcwd(), 'translation/', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    if args.execute_script_path is None:
        args.execute_script_path = "translation/execute_java_kc_local.sh"
    if args.sandbox is None:
        args.sandbox = 0
    if args.temperature is None:
            args.temperature = 0.2

    if int(args.sandbox) == 1:
        mixed_modality_translate(
            files=args.files,
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            error_path="ConvertedCode/converted.txt",
            testFiles=args.test_files,
            input_dir_test=args.input_dir_test,
            temp=float(args.temperature),
        )
    else:
        llm_translate(
            files=args.files,
            input_dir=args.input_dir,
            output_dir=args.output_dir,
            execute_script_path=args.execute_script_path,
            error_path="ConvertedCode/converted.txt",
            testFiles=args.test_files,
            input_dir_test=args.input_dir_test,
            temp=float(args.temperature),
        )

    #e.g.
    #python3 translation/translate.py --files Task TaskManager --input_dir LLM-Evaluation/src/main/org/cornell/ --test_files TaskManagerTest --input_dir_test LLM-Evaluation/src/test/java/
    #sandbox code:
    #python3 translation/translate.py --files AccurateMath AccurateMathCalc  --input_dir commons-math/commons-math-core/src/main/java/org/apache/commons/math4/core/jdkmath/ --test_files AccurateMathTest --input_dir_test ConvertedCode/ --sandbox 1


#     llm_translate(files, input_dir, output_dir, execute_script_path, error_path, testFiles, input_dir_test)
#     mutation_test(args.files, args.test_files, args.output_dir, 3, 3, "ConvertedCode/converted.txt")
