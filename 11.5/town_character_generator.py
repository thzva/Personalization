import os
import json as json_module
from openai import OpenAI
from datetime import datetime
import random

# 代理和API密钥设置
os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ['OPENAI_API_KEY'] = ' OPENAI_API_KEY'

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def load_profile_schema():
    """加载用户档案模式"""
    try:
        with open('user-profile.json', 'r', encoding='utf-8') as file:
            return json_module.load(file)
    except Exception as e:
        print(f"Error loading schema: {e}")
        return {}

def create_profile_prompt(profile_number, existing_profiles, schema):
    """创建生成用户档案的prompt"""
    # 构建现有角色的关系网络描述
    existing_chars_desc = ""
    if existing_profiles:
        existing_chars_desc = "\nExisting characters in the town:\n"
        for prof in existing_profiles:
            profile_data = prof["profile"]
            demo_info = profile_data.get("demographicInformation", {})
            name = demo_info.get("name", "Unknown")
            age = demo_info.get("age", "Unknown")
            occupation = demo_info.get("occupation", "Unknown")
            
            existing_chars_desc += f"- {name} (Age: {age}): {occupation}\n"
            if "relationships" in profile_data:
                for rel in profile_data["relationships"]:
                    existing_chars_desc += f"  → Knows {rel.get('name', 'Unknown')} as {rel.get('relationshipType', 'Unknown')}\n"

    prompt = f"""Create character #{profile_number} for our small town community using the provided user profile schema.

Reference Schema:
{json_module.dumps(schema, indent=2)}

Task Requirements:
1. This is character #{profile_number} in our small town.
2. Select and fill relevant fields from the schema that best define this character.
3. You don't need to fill all fields - choose those that help create a vivid, realistic person.
4. Make the character unique and memorable while maintaining realistic small-town dynamics.
5. If this isn't the first character, create meaningful connections with at least one existing character.

{existing_chars_desc}

Special Instructions:
- Choose fields that best tell this character's story
- Create realistic relationships appropriate for a small town setting
- Consider how this character fits into the town's social fabric
- Include any unique traits or characteristics that make them memorable

Return ONLY a JSON object with your selected fields filled in appropriately. Include a 'relationships' array for connections to other characters."""

    return prompt

def chat_with_GPT(conversation):
    """调用GPT API生成响应"""
    return client.chat.completions.create(
        messages=conversation,
        model="gpt-4-turbo-preview",
        temperature=0.8,
        max_tokens=2000
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
        print("Response text:", response_text[:200] + "...")
        return None

def save_results(results, filename="town_characters.json"):
    """保存结果到JSON文件"""
    with open(filename, 'w', encoding='utf-8') as file:
        json_module.dump(results, file, indent=2, ensure_ascii=False)

def generate_town_characters(num_profiles=150):
    """生成小镇角色档案"""
    results = []
    schema = load_profile_schema()
    
    for i in range(num_profiles):
        print(f"\nGenerating character {i+1}/{num_profiles}...")
        
        # 创建prompt并获取响应
        prompt = create_profile_prompt(i+1, results, schema)
        conv = [{"role": "user", "content": prompt}]
        
        try:
            reply = chat_with_GPT(conv)
        except Exception as e:
            print(f"Error in API call: {e}")
            continue
        
        if not reply:
            print(f"Error generating character {i+1}")
            continue
        
        # 解析响应
        profile = parse_gpt_response(reply)
        if profile:
            # 添加生成时间戳和角色ID
            result = {
                "characterId": f"TC{i+1:03d}",
                "timestamp": datetime.now().isoformat(),
                "profile": profile
            }
            results.append(result)
            
            # 保存当前进度
            save_results(results)
            print(f"Character {i+1} generated and saved")
            
            # 打印预览
            demo_info = profile.get("demographicInformation", {})
            preview = {
                "characterId": f"TC{i+1:03d}",
                "name": demo_info.get("name", "Unknown"),
                "age": demo_info.get("age", "Unknown"),
                "occupation": demo_info.get("occupation", "Unknown"),
                "relationships": profile.get("relationships", [])
            }
            print("\nCharacter Preview:")
            print(json_module.dumps(preview, indent=2, ensure_ascii=False))
        else:
            print(f"Error parsing character {i+1}")
    
    return results

if __name__ == "__main__":
    print("Starting small town character generation...")
    try:
        results = generate_town_characters(150)
        print(f"\nGeneration complete. Total characters generated: {len(results)}")
        print("All characters saved to town_characters.json")
    except Exception as e:
        print(f"An error occurred: {e}")