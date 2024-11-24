import os
import json
from openai import OpenAI


os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ['OPENAI_API_KEY'] = 'OPENAI-API-KEY'

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def chat_with_GPT(conversation):    
    response = client.chat.completions.create(
        messages=conversation,
        model="gpt-4o",
    )
    return response.choices[0].message.content

def evaluate_user_profile(profile):
    prompt = (
        f"Please evaluate if the following user profile is reasonable. "
        f"If reasonable, output 'OK'. If not, describe the issues. "
        f"If the user profile evaluation is reasonable, there is no need to provide a justification."
        f"Profile: {json.dumps(profile, indent=2)}"
    )
    total_message = [{"role": "user", "content": prompt}]
    result = chat_with_GPT(total_message)
    return result.strip()

if __name__ == "__main__":
    input_file = "cleaned_user_profiles.json"
    output_file = "profile_evaluation_results.json"

    with open(input_file, "r", encoding="utf-8") as f:
        user_profiles = json.load(f)  

    results = {}
    for index, profile in enumerate(user_profiles):  
        evaluation_result = evaluate_user_profile(profile)
        results[f"user_{index}"] = evaluation_result


    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Evaluation results saved to {output_file}")