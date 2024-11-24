import json

# 假设原始 JSON 文件名为 'data.json'
input_file = 'cleaned_user_profiles.json'
output_file = 'hobbies_interests_and_lifestyle.json'

# 读取原始 JSON 数据
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 初始化提取数据的字典
hobbies_data = {}

# 遍历所有用户数据
for user in data:
    if 'persona' in user and 'name' in user['persona']:
        # 获取用户名字作为唯一标识符
        user_name = user['persona']['name']
        # 提取 hobbies_interests_and_lifestyle 字段
        hobbies = {}
        for key, value in user['persona'].items():
            if key.startswith('hobbies_interests_and_lifestyle'):
                hobbies[key] = value
        # 将数据存储到结果字典中
        if hobbies:
            hobbies_data[user_name] = hobbies

# 将提取的数据保存到新的 JSON 文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(hobbies_data, f, ensure_ascii=False, indent=4)

# 打印统计信息
print(f"Extracted hobbies and interests for {len(hobbies_data)} users.")