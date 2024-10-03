from openai import OpenAI
import os

# completion = response.parse()  # get the object that `chat.completions.create()` would have returned
# print(completion)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        # if we wanna skip the system role and negate prompt enginering we can skip the system role step
        # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
        # 		{
        # 			"role": "system",
        # 			"content": "You are a helpful assistant for solving math word problems that formats the numerical answer with '####' preceding it at the end"
        # 		},
        {
            "role": "user",
            "content": "Janet\u2019s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?"
        },
    ]
)

print(completion.choices[0].message.content)

# CURRENTLY NO PROMPT ENGINEERING!
# def genResponses(file, first_five=True):
#     client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
#     f = open(file)
#     data = json.load(f)    f = open(file)
#                              data = json.load(f)
#     dic = {}
#     total = len(data.keys())
#
#     # just for testing
#     if first_five:
#         total = 5
#     # print(total)
#     for i in range(total):
#         print(i)
#
#         if str(i) in data and 'question' in data[str(i)]:
#             message = data[str(i)]['question']
#             # print(message)
#
#             re.sub("<<.*?>>", "", message)
#             completion = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[
#                     # if we wanna skip the system role and negate prompt enginering we can skip the system role step
#                     # {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
#                     {
#                         "role": "system",
#                         "content": "You are a helpful assistant for solving math word problems that formats the numerical answer with '####' preceding it at the end"
#                     },
#                     {
#                         "role": "user",
#                         "content": "Janet\u2019s ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?"
#                     },
#                     {
#                         "role": "assistant",
#                         "content": "Janet sells 16 - 3 - 4 = 9 duck eggs a day.\nShe makes 9 * 2 = $18 every day at the farmer\u2019s market.\n#### 18"
#                     },
#                     {"role": "user", "content": message}
#                 ]
#             )
#             rTuple = {}
#             rTuple['message'] = message
#             rTuple['response'] = completion.choices[0].message.content
#             dic[str(i)] = rTuple
#     return dic
#
# # saving the response
#
#
# def saveResponses(file, data):
#     with open(file, 'w') as fp:
#         json.dump(data, fp)
#
#
# test_responses = genResponses('data/GSM8K_raw/test.json', first_five=False)
# saveResponses('data/GSM8K_raw/test_responses_full2.json', test_responses)