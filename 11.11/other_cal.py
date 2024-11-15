import json
import numpy as np
from sentence_transformers import SentenceTransformer
from itertools import combinations
from tqdm import tqdm

# 加载模型
print("Loading model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# 读取处理后的数据
print("Loading data...")
with open('hyr_cleaned.json', 'r', encoding='utf-8') as f:
    profiles = json.load(f)

categories = [
    'physical_and_health_characteristics',
    'psychological_and_cognitive_aspects',
    'cultural_and_social_context',
    'relationships_and_social_networks', 
    'career_and_work_identity',
    'education_and_learning',
    'hobbies_interests_and_lifestyle',
    'lifestyle_and_daily_routine',
    'core_values_beliefs_and_philosophy',
    'emotional_and_relational_skills',
    'media_consumption_and_engagement'
]

# 创建结果字典
similarity_results = {category: [] for category in categories}

# 计算总的比较次数
total_comparisons = len(list(combinations(profiles, 2))) * len(categories)

# 创建总进度条
with tqdm(total=total_comparisons, desc="Computing similarities") as pbar:
    # 对每个类别计算相似度
    for category in categories:
        # 获取所有用户对的组合
        for person1, person2 in combinations(profiles, 2):
            # 获取两个人在该类别的描述
            text1 = person1.get(category, '')
            text2 = person2.get(category, '')
            
            similarity_entry = {
                "person1": person1["name"],
                "person2": person2["name"]
            }
            
            # 如果两个人都有该类别的描述，计算相似度
            if text1 and text2:
                # 计算嵌入向量
                embeddings = model.encode([text1, text2])
                # 计算余弦相似度
                similarity = np.dot(embeddings[0], embeddings[1]) / (
                    np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
                )
                similarity_entry["similarity"] = float(similarity)
            else:
                similarity_entry["similarity"] = 0
            
            similarity_results[category].append(similarity_entry)
            pbar.update(1)

print("Saving results...")
# 写入结果到新的json文件
with open('similarity.json', 'w', encoding='utf-8') as f:
    json.dump(similarity_results, f, indent=2, ensure_ascii=False)

print("Done!")