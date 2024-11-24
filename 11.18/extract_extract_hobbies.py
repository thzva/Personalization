import json

# 输入文件和输出文件名
input_file = 'hobbies_interests_and_lifestyle.json'
output_file = 'formatted_hobbies_interests_and_lifestyle.json'

# 读取 JSON 数据
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 转换数据格式
formatted_data = {}

for name, hobbies in data.items():
    # 提取每个用户所有兴趣的值，并处理列表和字符串
    combined_hobbies = []
    for value in hobbies.values():
        if isinstance(value, list):  # 如果是列表，合并为字符串
            combined_hobbies.append(", ".join(value))
        elif isinstance(value, str):  # 如果是字符串，直接添加
            combined_hobbies.append(value)
    # 合并所有兴趣项为单个字符串
    formatted_data[name] = ",".join(combined_hobbies)

# 保存到新的 JSON 文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(formatted_data, f, ensure_ascii=False, indent=4)

# 打印完成信息
print(f"Formatted hobbies and interests saved to {output_file}.")