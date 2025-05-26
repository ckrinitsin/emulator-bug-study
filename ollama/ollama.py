from ollama import chat, ChatResponse

model = "deepseek-r1:70b"

response: ChatResponse = chat(
    model=model, messages=[
        {
            'role': 'user',
            'content': 'Hello, how are you?',
        }
    ],
    stream=True
)

for chunk in response:
    print(chunk['message']['content'], end='', flush=True)
print("\n")
