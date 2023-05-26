import openai

from token_1 import OpenAI_Token

openai.api_key = OpenAI_Token

def get_chat(query:str) -> str:
    model = "gpt-3.5-turbo"
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    answer = response['choices'][0]['message']['content']
    return answer