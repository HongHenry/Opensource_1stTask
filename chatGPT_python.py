#Using ChatGPT in Python

import os
import openai

openai.api_key = "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"
question = input("무엇을 물어볼까요?\n")

completion = openai.ChatCompletion.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role":"user", "content" : question}
    ]
)

print(completion.choices[0].message.content)