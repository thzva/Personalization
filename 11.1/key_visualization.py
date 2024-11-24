import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def create_similarity_heatmap():
    # 读取数据
    print("正在读取数据...")
    with open('key_similarity.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取所有独特的人名
    print("正在处理人名...")
    all_names = set()
    for item in data['similarities']:
        all_names.add(item['person1'])
        all_names.add(item['person2'])
    all_names = sorted(list(all_names))
    print(f"共找到 {len(all_names)} 个独特的人名")
    
    # 创建矩阵
    n = len(all_names)
    interests_matrix = np.zeros((n, n))
    lifestyle_matrix = np.zeros((n, n))
    
    # 填充矩阵
    print("正在创建相似度矩阵...")
    name_to_index = {name: i for i, name in enumerate(all_names)}
    for item in data['similarities']:
        i = name_to_index[item['person1']]
        j = name_to_index[item['person2']]
        interests_matrix[i, j] = item['interests_similarity']
        interests_matrix[j, i] = item['interests_similarity']
        lifestyle_matrix[i, j] = item['lifestyle_similarity']
        lifestyle_matrix[j, i] = item['lifestyle_similarity']
    
    # 设置对角线为1
    np.fill_diagonal(interests_matrix, 1.0)
    np.fill_diagonal(lifestyle_matrix, 1.0)
    
    # 创建图形
    print("正在创建热力图...")
    plt.figure(figsize=(20, 8))
    
    # 创建子图
    plt.subplot(1, 2, 1)
    sns.heatmap(interests_matrix, 
                annot=True, 
                fmt='.2f', 
                cmap='YlOrRd', 
                xticklabels=all_names, 
                yticklabels=all_names)
    plt.title('Interest Similarity Heatmap')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    plt.subplot(1, 2, 2)
    sns.heatmap(lifestyle_matrix, 
                annot=True, 
                fmt='.2f', 
                cmap='YlOrRd', 
                xticklabels=all_names, 
                yticklabels=all_names)
    plt.title('Lifestyle Similarity Heatmap')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # 调整布局
    plt.tight_layout()
    
    # 保存图片
    print("正在保存图片...")
    plt.savefig('key_similarity_heatmap.png', 
                dpi=300, 
                bbox_inches='tight',
                pad_inches=0.5)
    plt.close()
    
    print("成功保存热力图到 key_similarity_heatmap.png")

if __name__ == "__main__":
    print("开始生成热力图...")
    create_similarity_heatmap()