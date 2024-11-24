import os
from openai import OpenAI


os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)



def chat_with_GPT(conversation):    #chat with gpt api
    response=client.chat.completions.create(
    messages=conversation,
    model="chatgpt-4o-latest",
    )
    return response.choices[0].message.content


def conversation(prompt):       # save the total conversation
    total_message.append({"role":"user","content": prompt})
    return total_message


def agent1():                    #news agent1
    prompt = input("")
    if prompt == 'stop':
        return None
    reply = chat_with_GPT(conversation(prompt))
    print(reply)
    viewpoint1 = conversation(reply)
    return viewpoint1



if __name__ == "__main__":
  print("Please input your prompt")
  total_message = []           #input datatype
  while True:
    viewpoint1 = agent1()