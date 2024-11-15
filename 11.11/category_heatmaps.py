import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

# 读取相似度数据
with open('similarity.json', 'r', encoding='utf-8') as f:
    similarity_data = json.load(f)

# 获取所有唯一的人名
all_names = set()
for category in similarity_data:
    for entry in similarity_data[category]:
        all_names.add(entry['person1'])
        all_names.add(entry['person2'])
all_names = sorted(list(all_names))

# 创建一个函数来构建热力图矩阵
def create_heatmap_matrix(category_data, names):
    n = len(names)
    matrix = np.ones((n, n))
    
    name_to_idx = {name: i for i, name in enumerate(names)}
    
    for entry in category_data:
        if entry['similarity'] != "NAN":
            i = name_to_idx[entry['person1']]
            j = name_to_idx[entry['person2']]
            matrix[i, j] = entry['similarity']
            matrix[j, i] = entry['similarity']
    
    return matrix

# 设置全局字体大小
plt.rcParams.update({'font.size': 12})

# 创建子图网格
n_rows = 4
n_cols = 3
fig = plt.figure(figsize=(20, 25))

# 为每个类别创建热力图
for idx, category in enumerate(tqdm(similarity_data.keys(), desc="Creating heatmaps")):
    matrix = create_heatmap_matrix(similarity_data[category], all_names)
    
    plt.subplot(n_rows, n_cols, idx + 1)
    
    sns.heatmap(
        matrix,
        cmap='coolwarm',
        vmin=0,
        vmax=1,
        annot=False,
        fmt='.2f',
        square=True,
        xticklabels=False,
        yticklabels=False,
        cbar_kws={
            'label': 'Similarity Score',
            'shrink': 0.8,
            'aspect': 20,
            'pad': 0.02
        }
    )
    
    plt.title(f'{category}', pad=20, fontsize=14)

plt.tight_layout()
plt.savefig('category_heatmaps.png', dpi=300, bbox_inches='tight')
plt.close()

print("热力图已保存为 category_heatmaps.png")