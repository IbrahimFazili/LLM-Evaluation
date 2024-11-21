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

def gen_llm_output_java2python(input_path, output_path, temp=None, history=BASE_SETUP, feedback=False):
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
            errors = detect_error_in_file(input_path)
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

def feedback_loop(error_path, files, response_history, output_dir):
    for file in files:
        response_history[file] = gen_llm_output_java2python(error_path, output_dir + "/" + file + ".py", temp = 0, history=response_history[file], feedback=True)
        shutil.copyfile(output_dir + "/" + file + '.py', 'temp/' + file + '.py')
    return response_history



def save_outputs(files, input_dir, output_dir, response_history=None):
    #we want to keep a tally of the histories for each of the responses
    if not response_history:
        response_history = {}
    for file in files:
        response_history[file] = gen_llm_output_java2python(input_dir + file + '.java', output_dir + "/" + file + '.py', temp=0)
        shutil.copyfile(output_dir + "/" + file + '.py', 'temp/' + file + '.py')
        print(f'Generated file: {file}')
    return response_history



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
    with open(output_dir+f'/run{run_no}/'+"response_history.txt", 'w') as f:
        print(response_history, file=f)
    #
    print("Checking answers")
    subprocess.run(execute_script_path, shell=True, capture_output=True, text=True)
    errors = detect_error_in_file(error_path)
    shutil.copyfile(error_path, output_dir+f'/run{run_no}/'+"error_output.txt")
    return errors

def llm_translate(files, input_dir, output_dir, execute_script_path, error_path, num_of_retries=5):
    os.makedirs(output_dir)
    run_no = 1
    os.makedirs(output_dir + f'/run{run_no}/')
    response_history = save_outputs(files, input_dir, output_dir+f'/run{run_no}/')
    if num_of_retries > 0:
        errors = check_translation(execute_script_path, output_dir, run_no, response_history, error_path)
        while errors:
            print("ENTERING FEEDBACK LOOP")
            if run_no == num_of_retries:
                break
            run_no += 1
            print(f'on feedback loop number {run_no-1}')
            print(f'Number of errors: {len(errors)}')
            os.makedirs(output_dir + f'/run{run_no}/')
            response_history = feedback_loop(error_path, files, response_history, output_dir+f'/run{run_no}/')
            errors = check_translation(execute_script_path, output_dir, run_no, response_history, error_path)

        if not errors:
            print(f'Number of errors: 0')
            print("SUCCESSFULLY TRANSLATED!")
        else:
            print(f'Number of errors: {len(errors)}')
            print("WOMP WOMP :(")
    else:
        print("NOT ENTERING FEEDBACK LOOP")

    return response_history
if __name__ == "__main__":
    #files should only correspond to the files within a given package

    files = ["Task", "TaskManager"]
    input_dir = 'LLM-Evaluation/src/main/org/cornell/'
    output_dir = os.path.join(os.getcwd(), 'translation/', datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    execute_script_path = "translation/execute_java_kc_local.sh"
    error_path = "ConvertedCode/converted.txt"
    #

    llm_translate(files, input_dir, output_dir, execute_script_path, error_path)

