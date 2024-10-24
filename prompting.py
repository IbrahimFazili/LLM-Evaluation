from openai import OpenAI
import os

CLIENT = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
SYSTEM_PROMPT = "You are a coding assistant, skilled in translating classes from Java into Python. Specifically you take in Java code and output Python code. Please only output Python code and keep the class name the same. Do not include '``` python' or '```' delimiters for the generated code block."
#in your env if you don't have the OPENAI_API_KEY env variable, run in your terminal:
#`export OPENAI_API_KEY=XXXX_XXX_XX_XXX` where the XXXX_XXX_XX_XXX is a valid openai api key



def send_to_llm(input_string, system_prompt):
    completion = CLIENT.chat.completions.create(
        model="gpt-4o-mini",
        messages=[

            {"role": "system", "content": system_prompt},
            #could maybe add in context examples for one/multishot prompting
            {
                "role": "user",
                "content": input_string
            },
        ]
    )
    return completion



#simple example (source code)
file_path = 'LLM-Evaluation/src/main/org/cornell/Math.java'
try:
    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Read the file content
        java_code = file.read()

    response = send_to_llm(java_code, SYSTEM_PROMPT)
    response_output = response.choices[0].message.content
    # print(response_output)
    with open('math3.py', 'w') as f:
        print(response_output, file=f)
except Exception as e:
    print(f'Error reading file: {e}')

#simple example 2 (source code test)
file_path_test = 'LLM-Evaluation/src/test/java/MathTest.java'
try:
    # Open the file in read mode
    with open(file_path_test, 'r') as file:
        # Read the file content
        java_code = file.read()

    response = send_to_llm(java_code, SYSTEM_PROMPT)
    response_output = response.choices[0].message.content
    # print(response_output)
    with open('math_test.py', 'w') as f:
        print(response_output, file=f)


except Exception as e:
    print(f'Error reading file: {e}')