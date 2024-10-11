from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
#in your env if you don't have the OPENAI_API_KEY env variable, run in your terminal:
#`export OPENAI_API_KEY=XXXX_XXX_XX_XXX` where the XXXX_XXX_XX_XXX is a valid openai api key


completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        # if we want to skip the system role and negate prompt enginering we can skip the system role step
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
#next steps would be to prompt engineer some translating code tasks

print(completion.choices[0].message.content)
