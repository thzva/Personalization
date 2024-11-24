import json

# 文件路径
original_file = 'cleaned_user_profiles.json'  # 原始文件
extracted_file = 'formatted_hobbies_interests_and_lifestyle.json'  # 提取后的文件

# 读取 JSON 数据
with open(original_file, 'r', encoding='utf-8') as f:
    original_data = json.load(f)

with open(extracted_file, 'r', encoding='utf-8') as f:
    extracted_data = json.load(f)

# 获取原始文件中的用户名字
original_names = {user['persona']['name'] for user in original_data if 'persona' in user and 'name' in user['persona']}

# 获取提取后的文件中的用户名字
extracted_names = set(extracted_data.keys())

# 查找缺失的用户名字
missing_names = original_names - extracted_names

# 打印结果
if not missing_names:
    print("OK")
else:
    print("Missing users:")
    for name in missing_names:
        print(name)