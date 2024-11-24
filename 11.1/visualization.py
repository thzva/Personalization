import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def create_heatmap():
    # 读取相似度数据
    with open('similarity_results.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 获取数据
    names = data['names']
    similarity_matrix = np.array(data['similarity_matrix'])
    
    # 设置图片大小和DPI
    plt.figure(figsize=(12, 10), dpi=300)
    
    # 创建热力图
    sns.heatmap(
        similarity_matrix,
        xticklabels=names,
        yticklabels=names,
        cmap='Reds',  # 使用红色渐变色
        annot=True,   # 显示数值
        fmt='.2f',    # 数值保留两位小数
        square=True,  # 保持单元格为正方形
        cbar_kws={'label': '相似度'}  # 颜色条标签
    )
    
    # 设置标题和标签
    plt.title('用户相似度热力图', fontsize=16, pad=20)
    plt.xlabel('用户', fontsize=12, labelpad=10)
    plt.ylabel('用户', fontsize=12, labelpad=10)
    
    # 调整布局，确保标签不被截断
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    # 保存图片
    plt.savefig('similarity_heatmap.png', bbox_inches='tight', dpi=300)
    plt.close()
    
    print("热力图已保存为 similarity_heatmap.png")

if __name__ == "__main__":
    try:
        create_heatmap()
    except FileNotFoundError:
        print("错误：找不到 similarity_results.json 文件")
    except json.JSONDecodeError:
        print("错误：similarity_results.json 文件格式不正确")
    except Exception as e:
        print(f"生成热力图时出错：{str(e)}")