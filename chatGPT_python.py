import openai
import time

# OpenAI API Key 설정
openai.api_key = "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"

# 대화를 시작합니다.
def start_chat(prompt):
    # Chat GPT API를 이용하여 응답을 생성합니다.
    response = openai.Completion.create(
        engine="davinci", # API 엔진 선택
        prompt=prompt, # 대화 시작 문장
        max_tokens=60, # 생성할 최대 토큰 개수
        n=1, # 생성할 문장 개수
        stop=None, # 응답 생성을 멈출 텍스트
        temperature=0.5 # 높을수록 새로운 문장 생성 가능성이 높아집니다.
    )

    # 생성된 문장 중 첫 번째 문장을 반환합니다.
    message = response.choices[0].text.strip()

    return message

# 채팅 시작
while True:
    prompt = input("사용자: ")
    response = start_chat(prompt)
    print("챗봇: " + response)
    time.sleep(1)
