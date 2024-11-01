import os
import json as json_module
from openai import OpenAI
import random
from datetime import datetime

# 代理和API密钥设置
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
    base_url="https://api.openai.com/v1",
)

def create_profile_prompt(profile_number):
    """优化的prompt以确保正确的JSON输出"""
    return f"""Output a valid JSON object for profile {profile_number} exactly matching this structure, with no additional text or explanations:

{{
    "basicPersonalInformation": {{
        "fullName": {{
            "firstName": "string",
            "middleName": "string",
            "lastName": "string"
        }},
        "dateOfBirth": "DD/MM/YYYY",
        "gender": "Male|Female|Non-binary|Prefer not to say",
        "maritalStatus": "Single|Married|Divorced|Widowed|Partnered"
    }},
    "additionalPersonalInformation": {{
        "nationality": "string",
        "ethnicity": "string",
        "languagesSpoken": ["string", "string"],
        "preferredPronouns": "string",
        "countryOfResidence": "string",
        "cityOfResidence": "string"
    }},
    "educationalInformation": {{
        "highestEducationLevel": "string",
        "institutionsAttended": [
            {{
                "instituteName": "string",
                "degree": "string",
                "fieldOfStudy": "string",
                "startDate": "string",
                "endDate": "string"
            }}
        ]
    }},
    "professionalInformation": {{
        "currentOccupation": "string",
        "employer": "string",
        "industry": "string",
        "skills": ["string", "string"],
        "experienceLevel": "string",
        "workHistory": ["string"]
    }},
    "preferencesAndInterests": {{
        "hobbiesAndInterests": ["string", "string"],
        "contentPreferences": ["string", "string"],
        "shoppingPreferences": {{
            "preferredBrands": ["string", "string"],
            "productTypes": ["string", "string"],
            "priceRanges": ["string", "string"]
        }},
        "learningPreferences": ["string", "string"],
        "dietaryPreferences": ["string", "string"]
    }},
    "psychographicInformation": {{
        "personalityTraits": ["string", "string"],
        "temperament": "string",
        "characterStrengths": ["string", "string"],
        "values": ["string", "string"],
        "purposeAndMeaning": "string",
        "motivationAndDesires": ["string", "string"],
        "lifestyle": {{
            "dailyHabits": ["string", "string"],
            "healthGoals": ["string", "string"],
            "politicalSocialBeliefs": ["string", "string"]
        }}
    }},
    "fitness": {{
        "healthGoals": ["string", "string"],
        "medicalConditions": ["string"],
        "exercisePreferences": ["string", "string"]
    }},
    "politicalViews": "string",
    "onlinePresence": {{
        "groupsAndCommunities": ["string", "string"],
        "technologyUsage": {{
            "platforms": ["string", "string"],
            "tools": ["string", "string"]
        }}
    }}
}}"""

def chat_with_GPT(conversation):
    """增强的GPT API调用，使用更高的创造性参数"""
    try:
        # 为每次调用随机化参数以增加多样性
        temperature = random.uniform(0.8, 0.95)  # 提高温度以增加创造性
        max_tokens = random.randint(2000, 3000)  # 允许更长的响应
        presence_penalty = random.uniform(0.5, 0.8)  # 显著降低重复
        frequency_penalty = random.uniform(0.3, 0.6)  # 鼓励使用更多样的词汇
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": """You are a creative JSON generator that creates highly diverse and unique user profiles. 
                    Each profile should be distinctly different from others in terms of:
                    - Demographics and background
                    - Education and career paths
                    - Interests and preferences
                    - Personality traits and values
                    - Cultural and social perspectives
                    Ensure maximum variety while maintaining realism and consistency within each profile."""
                },
                *conversation
            ],
            model="gpt-4",
            temperature=temperature,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty
        )    
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in API call: {str(e)}")
        return None

def parse_gpt_response(response_text):
    """改进的JSON解析函数"""
    try:
        # 移除任何非JSON内容
        content = response_text.strip()
        start_idx = content.find('{')
        end_idx = content.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            content = content[start_idx:end_idx + 1]
            
            # 清理常见的格式问题
            content = content.replace('\n', ' ')
            content = content.replace('\r', '')
            content = content.replace('\\', '')
            
            # 解析JSON
            return json_module.loads(content)
    except Exception as e:
        print(f"Error parsing response: {str(e)}")
        print("Response content:")
        print(response_text[:200] + "..." if len(response_text) > 200 else response_text)
        return None

def save_results(results, filename="results.json"):
    """保存结果到JSON文件"""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json_module.dump(results, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving results: {str(e)}")

def generate_batch_profiles(num_profiles=20):
    """生成批量用户档案"""
    results = []
    retry_count = 3  # 每个配置文件的最大重试次数
    
    for i in range(num_profiles):
        success = False
        attempts = 0
        
        while not success and attempts < retry_count:
            print(f"\nGenerating profile {i+1}/{num_profiles} (Attempt {attempts+1}/{retry_count})...")
            
            try:
                # 创建prompt并获取响应
                conv = [{"role": "user", "content": create_profile_prompt(i+1)}]
                reply = chat_with_GPT(conv)
                
                if not reply:
                    print(f"No response from API for profile {i+1}")
                    attempts += 1
                    continue
                
                # 解析响应
                profile = parse_gpt_response(reply)
                if profile:
                    result = {
                        "timestamp": datetime.now().isoformat(),
                        "profile": profile
                    }
                    results.append(result)
                    save_results(results)  # 保存当前进度
                    print(f"Profile {i+1} generated and saved successfully")
                    
                    # 打印部分生成的内容以供验证
                    print("\nProfile preview:")
                    preview = {
                        "basicPersonalInformation": profile["basicPersonalInformation"],
                        "additionalPersonalInformation": profile["additionalPersonalInformation"]
                    }
                    print(json_module.dumps(preview, indent=2, ensure_ascii=False))
                    
                    success = True
                else:
                    print(f"Failed to parse profile {i+1}")
                    attempts += 1
            except Exception as e:
                print(f"Error generating profile {i+1}: {str(e)}")
                attempts += 1
        
        if not success:
            print(f"Failed to generate profile {i+1} after {retry_count} attempts")
            continue
            
    
    return results

if __name__ == "__main__":
    try:
        print("Starting batch profile generation...")
        print("This will generate 20 unique user profiles and save them to results.json")
        print("Press Ctrl+C to stop at any time. Progress is saved after each successful generation.\n")
        
        results = generate_batch_profiles(20)
        
        print(f"\nGeneration complete. Total profiles generated: {len(results)}")
        print("All results saved to results.json")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Saving current progress...")
        print("Any successfully generated profiles have been saved to results.json")
    except Exception as e:
        print(f"Error in main execution: {str(e)}")