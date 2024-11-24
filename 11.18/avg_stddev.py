import json
import numpy as np
import matplotlib.pyplot as plt

# 读取json文件
with open('similarity.json', 'r') as f:
   data = json.load(f)

categories = ['demographic_information', 'physical_and_health_characteristics',                'psychological_and_cognitive_aspects', 'cultural_and_social_context',               'relationships_and_social_networks', 'career_and_work_identity',               'education_and_learning', 'hobbies_interests_and_lifestyle',               'lifestyle_and_daily_routine', 'core_values_beliefs_and_philosophy',               'emotional_and_relational_skills', 'media_consumption_and_engagement'] 

# 计算每个category的统计信息
stats = {}
for category in categories:
   similarities = [item['similarity'] for item in data[category]]
   stats[category] = {
       'avg': np.mean(similarities),
       'stddev': np.std(similarities),
       'avg/stddev': np.mean(similarities) / np.std(similarities)
   }

# 提取categories和对应的avg/stddev值
categories_short = [cat.replace('_', '\n') for cat in categories]  # 换行显示长category名
ratios = [stats[cat]['avg/stddev'] for cat in categories]

# 创建柱状图
plt.figure(figsize=(12, 6))
plt.bar(categories_short, ratios)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Average/Standard Deviation')
plt.title('Average/Standard Deviation Ratio by Category')

# 调整布局避免标签被截断
plt.tight_layout()

plt.savefig('category_ratios.png', bbox_inches='tight', dpi=300)