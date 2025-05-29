from ollama import chat, ChatResponse
from re import sub
from os import listdir, path

model : str = "deepseek-r1:70b"
directory : str = "../mailinglist/output_mailinglist"

with open("preambel", "r") as file:
    preambel = file.read()

for name in listdir(directory):
    with open(path.join(directory, name)) as file:
        content = preambel + "\n" + file.read()

    with open("test", "r") as file:
        content = file.read()

    response : ChatResponse = chat(
        model=model, messages=[
            {
                'role': 'user',
                'content': content,
            }
        ]
    )

    no_think_response : str = sub(r'<think>(.|\n)*</think>\n\n', '', response.message.content)

    print(no_think_response)
    print("\n")
    exit()
