import os
import json
from openai import OpenAI
from datetime import datetime

# 保持原有的代理和API配置
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def chat_with_GPT(conversation):
    response = client.chat.completions.create(
        messages=conversation,
        model="chatgpt-4o-latest",
    )
    return response.choices[0].message.content

def check_profile_coherence(profile_data):
    # 提取个人档案的关键信息用于简洁的提示
    basic_info = profile_data["profile"]["basicPersonalInformation"]
    prof_info = profile_data["profile"]["professionalInformation"]
    edu_info = profile_data["profile"]["educationalInformation"]
    
    summary = f"""
    Name: {basic_info['fullName']['firstName']} {basic_info['fullName']['lastName']}
    Birth: {basic_info['dateOfBirth']}
    Education: {edu_info['highestEducationLevel']} in {edu_info['institutionsAttended'][0]['fieldOfStudy']}
    Occupation: {prof_info['currentOccupation']} at {prof_info['employer']}
    Experience: {prof_info['experienceLevel']}
    """
    
    prompt = f"""Analyze this person's profile for logical consistency and coherence. 
    Consider:
    1. Age vs education/career timeline
    2. Skills vs education/experience
    3. Location consistency
    4. Professional progression
    5. Overall profile coherence
    
    Profile summary:
    {summary}
    
    Full profile data:
    {json.dumps(profile_data["profile"], indent=2)}
    
    Output only the number 1 if the profile is coherent and reasonable, or 2 if there are significant inconsistencies.
    """
    
    try:
        conversation = [
            {"role": "system", "content": "You are a profile analyzer that only outputs 1 or 2."},
            {"role": "user", "content": prompt}
        ]
        
        result = int(chat_with_GPT(conversation).strip())
        return result
        
    except Exception as e:
        print(f"Error during profile checking: {str(e)}")
        return None

def process_profiles():
    try:
        # 读取并解析JSON文件
        print("读取档案数据...")
        with open('results.json', 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        
        print(f"\n找到 {len(profiles)} 条档案")
        
        # 存储结果的列表
        check_results = []
        
        # 处理每个档案
        for i, profile in enumerate(profiles, 1):
            print(f"\n正在处理第 {i}/{len(profiles)} 条档案...")
            print(f"档案: {profile['profile']['basicPersonalInformation']['fullName']['firstName']} {profile['profile']['basicPersonalInformation']['fullName']['lastName']}")
            
            try:
                result = check_profile_coherence(profile)
                
                check_result = {
                    "timestamp": datetime.now().isoformat(),
                    "profile_name": f"{profile['profile']['basicPersonalInformation']['fullName']['firstName']} {profile['profile']['basicPersonalInformation']['fullName']['lastName']}",
                    "input_profile_timestamp": profile["timestamp"],
                    "coherence_check_result": result,
                    "result_meaning": "合理" if result == 1 else "不合理"
                }
                
                check_results.append(check_result)
                
                # 每处理一条就保存一次
                with open('check_results.json', 'w', encoding='utf-8') as f:
                    json.dump(check_results, f, ensure_ascii=False, indent=2)
                
                print(f"结果: {'合理' if result == 1 else '不合理'}")
                
            except Exception as e:
                print(f"处理档案时出错: {str(e)}")
                continue
        
        # 打印总结
        print("\n处理完成！总结:")
        coherent_count = sum(1 for r in check_results if r['coherence_check_result'] == 1)
        print(f"合理的档案数量: {coherent_count}")
        print(f"不合理的档案数量: {len(check_results) - coherent_count}")
        print(f"处理失败的档案数量: {len(profiles) - len(check_results)}")
        
        # 打印详细结果
        print("\n详细结果:")
        for result in check_results:
            print(f"姓名: {result['profile_name']}")
            print(f"结果: {result['result_meaning']}")
            print("---")
        
    except Exception as e:
        print(f"处理过程中出现错误: {str(e)}")

if __name__ == "__main__":
    process_profiles()