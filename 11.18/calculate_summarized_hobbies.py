from sentence_transformers import SentenceTransformer
import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 输入 JSON 文件路径
input_file = 'formatted_hobbies_interests_and_lifestyle.json'

# 加载 JSON 数据
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 合并每个用户的兴趣描述为一个整体
user_names = list(data.keys())
all_interests = list(data.values())

# 加载 SentenceTransformer 模型
model = SentenceTransformer('all-MiniLM-L6-v2')

# 计算每个兴趣的语义嵌入
embeddings = model.encode(all_interests, convert_to_tensor=True).cpu().numpy()

# 定义相似度阈值
similarity_threshold = 0.9

# 计算用户之间的相似度矩阵
similarity_matrix = cosine_similarity(embeddings)

# 找出兴趣相似的用户
similar_users = {}
unique_interests_count = len(user_names)  # 初始为用户数

for i in range(len(user_names)):
    for j in range(i + 1, len(user_names)):
        if similarity_matrix[i, j] > similarity_threshold:
            if user_names[i] not in similar_users:
                similar_users[user_names[i]] = []
            similar_users[user_names[i]].append(user_names[j])
            unique_interests_count -= 1  # 如果发现相似用户，唯一兴趣计数减少

# 打印兴趣总数
print(f"Total number of unique interests: {unique_interests_count}")

# 输出相似用户
if similar_users:
    print("Users with similar interests:")
    for user, similar_to in similar_users.items():
        print(f"{user} is similar to: {', '.join(similar_to)}")
else:
    print("No users with similar interests found.")