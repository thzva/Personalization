import os
import json
from openai import OpenAI


# 设置代理和 OpenAI API 密钥
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ['OPENAI_API_KEY'] = 'OPENAI-API-KEY'
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def chat_with_GPT(prompt):
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4o",
    )
    return response.choices[0].message.content


def read_json(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


# 自动生成问题和答案
def generate_qa_from_persona(persona_data, num_questions=10):
    prompt = (
        f"Based on the following persona data:\n\n{json.dumps(persona_data, indent=2)}\n\n"
        f"Generate {num_questions} personalized questions relevant to this user and provide one detailed response for each question. "
        f"The questions should be as diverse as possible."
    )
    
    response = chat_with_GPT(prompt)
    print("GPT Response:\n", response)  # 调试信息

    questions_and_answers = []
    
    for i, qa in enumerate(response.split("\n\n")):
        if "Question:" in qa and "Answer:" in qa:
            question = qa.split("Question:")[1].split("Answer:")[0].strip()
            answer_a = qa.split("Answer:")[1].strip()
            
            questions_and_answers.append({
                "question_id": str(i + 1),
                "question": question,
                "response_a": answer_a
            })
            if len(questions_and_answers) >= num_questions:
                break
    
    return questions_and_answers


if __name__ == "__main__":
    # 输入文件名
    input_file = "yufan_zhou.json"
    
    # 检查输入文件是否存在
    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist. Please provide a valid file.")
        exit(1)
    
    # 读取用户档案数据
    persona_data = read_json(input_file)
    
    # 根据用户档案生成问题与答案
    qa_data = generate_qa_from_persona(persona_data, num_questions=10)
    
    # 直接输出生成的问题与答案
    print("\nGenerated QA Pairs:")
    for qa in qa_data:
        print(f"Question ID: {qa['question_id']}")
        print(f"Question: {qa['question']}")
        print(f"Response: {qa['response_a']}")
        print("-" * 50)