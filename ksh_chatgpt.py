import os
import openai
openai.api_key = "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"
question = input("무엇을 물어볼까요?\n")

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": question}
  ]
)

ksh_question = completion.choices[0].message

openai.Image.create(
  prompt = ksh_question,
  n=1,
  size="1024x1024"
)
image_url = response['data'][0]['url']

print(image_url)
