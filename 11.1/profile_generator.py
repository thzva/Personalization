import os
import json as json_module
from openai import OpenAI
import random
from datetime import datetime

# 代理和API密钥设置
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def create_profile_prompt(profile_number):
    """创建生成用户档案的prompt"""
    return f"""Generate a complete user profile (Profile {profile_number}) with all fields filled in realistically and comprehensively. 
    
Each field must be filled with appropriate and realistic content:
- Fill all empty string fields with appropriate values
- Fill all empty arrays with at least 2-3 relevant items
- Ensure date formats are DD/MM/YYYY
- For gender and marital status, choose one value from the provided options
- Ensure all information is consistent throughout the profile

Required JSON structure for the response:
{{
    "basicPersonalInformation": {{
        "fullName": {{
            "firstName": "",
            "middleName": "",
            "lastName": ""
        }},
        "dateOfBirth": "DD/MM/YYYY",
        "gender": "SINGLE_VALUE",
        "maritalStatus": "SINGLE_VALUE"
    }},
    "additionalPersonalInformation": {{
        "nationality": "Country name",
        "ethnicity": "Specific ethnicity",
        "languagesSpoken": [],
        "preferredPronouns": "",
        "countryOfResidence": "",
        "cityOfResidence": ""
    }},
    "educationalInformation": {{
        "highestEducationLevel": "",
        "institutionsAttended": [
            {{
                "instituteName": "",
                "degree": "",
                "fieldOfStudy": "",
                "startDate": "",
                "endDate": ""
            }}
        ]
    }},
    "professionalInformation": {{
        "currentOccupation": "",
        "employer": "",
        "industry": "",
        "skills": [],
        "experienceLevel": "",
        "workHistory": []
    }},
    "preferencesAndInterests": {{
        "hobbiesAndInterests": [],
        "contentPreferences": [],
        "shoppingPreferences": {{
            "preferredBrands": [],
            "productTypes": [],
            "priceRanges": []
        }},
        "learningPreferences": [],
        "dietaryPreferences": []
    }},
    "psychographicInformation": {{
        "personalityTraits": [],
        "temperament": "",
        "characterStrengths": [],
        "values": [],
        "purposeAndMeaning": "",
        "motivationAndDesires": [],
        "lifestyle": {{
            "dailyHabits": [],
            "healthGoals": [],
            "politicalSocialBeliefs": []
        }}
    }},
    "fitness": {{
        "healthGoals": [],
        "medicalConditions": [],
        "exercisePreferences": []
    }},
    "politicalViews": "",
    "onlinePresence": {{
        "groupsAndCommunities": [],
        "technologyUsage": {{
            "platforms": [],
            "tools": []
        }}
    }}
}}

Provide only the JSON response, no additional text."""

# def chat_with_GPT(conversation):
#     """调用GPT API生成响应"""
#     try:
#         response = client.chat.completions.create(
#             messages=conversation,
#             model="chatgpt-4o-latest",
#             temperature=0.8,
#             max_tokens=2000
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         print(f"Error in API call: {e}")
#         return None


def chat_with_GPT(conversation, creativity_level='balanced'):
    """
    调用GPT API生成响应,提供不同程度的创造性输出
    
    Args:
        conversation: 对话历史记录列表
        creativity_level: 创造性程度 ['conservative', 'balanced', 'creative', 'highly_creative']
    
    Returns:
        str: GPT生成的响应内容
    """
    # 根据创造性程度设置不同的参数组合
    creativity_settings = {
        'conservative': {
            'temperature': 0.3,
            'top_p': 0.6,
            'frequency_penalty': 0.0,
            'presence_penalty': 0.0
        },
        'balanced': {
            'temperature': 0.7,
            'top_p': 0.9,
            'frequency_penalty': 0.2,
            'presence_penalty': 0.2
        },
        'creative': {
            'temperature': 1.0,
            'top_p': 1.0,
            'frequency_penalty': 0.5,
            'presence_penalty': 0.5
        },
        'highly_creative': {
            'temperature': 1.2,
            'top_p': 1.0,
            'frequency_penalty': 0.8,
            'presence_penalty': 0.8
        }
    }
    
    # 获取当前创造性设置
    settings = creativity_settings[creativity_level]
    
    return client.chat.completions.create(
        messages=conversation,
        model="chatgpt-4o-latest",
        max_tokens=2000,
        **settings
    ).choices[0].message.content


def parse_gpt_response(response_text):
    """解析GPT响应为JSON"""
    try:
        return json_module.loads(response_text)
    except json_module.JSONDecodeError:
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                return json_module.loads(json_str)
        except:
            pass
        print("Error parsing GPT response as JSON")
        return None

def save_results(results, filename="results.json"):
    """保存结果到JSON文件"""
    with open(filename, 'w', encoding='utf-8') as file:
        json_module.dump(results, file, indent=2, ensure_ascii=False)

def generate_batch_profiles(num_profiles=10):
    """生成指定数量的用户档案"""
    results = []
    
    for i in range(num_profiles):
        print(f"\nGenerating profile {i+1}/{num_profiles}...")
        
        # 创建prompt并获取响应
        conv = [{"role": "user", "content": create_profile_prompt(i+1)}]
        reply = chat_with_GPT(conv)
        
        if not reply:
            print(f"Error generating profile {i+1}")
            continue
        
        # 解析响应
        profile = parse_gpt_response(reply)
        if profile:
            result = {
                "timestamp": datetime.now().isoformat(),
                "profile": profile
            }
            results.append(result)
            
            # 保存当前进度
            save_results(results)
            print(f"Profile {i+1} generated and saved")
            
            # 打印当前生成的profile以供查看
            print("\nGenerated Profile:")
            print(json_module.dumps(profile, indent=2, ensure_ascii=False)[:500] + "...")
        else:
            print(f"Error parsing profile {i+1}")
    
    return results

if __name__ == "__main__":
    print("Starting batch profile generation...")
    results = generate_batch_profiles(10)
    print(f"\nGeneration complete. Total profiles generated: {len(results)}")
    print("All results saved to results.json")