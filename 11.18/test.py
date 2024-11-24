import json

# 读取 JSON 文件
with open('cleaned_user_profiles.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 创建一个集合来存储唯一属性
unique_attributes = set()

# 递归函数提取所有属性
def extract_keys(d, parent_key=''):
    for key, value in d.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        if isinstance(value, dict):
            extract_keys(value, full_key)
        else:
            unique_attributes.add(full_key)

# 遍历 JSON 数据（假设每个元素是一个用户数据字典）
for user_data in data:
    extract_keys(user_data)

# 打印所有唯一属性
for attribute in sorted(unique_attributes):
    print(attribute)