import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns

# 设置seaborn样式
sns.set_style("whitegrid")
sns.set_context("notebook")

class CharacterAnalyzer:
    def __init__(self, json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def extract_character_text(self, profile):
        """提取角色的文本描述"""
        texts = []
        user_profile = profile.get('userProfile', {})
        
        categories = [
            'demographicInformation',
            'psychologicalCognitiveAspects',
            'hobbiesInterests',
            'workAndCareerIdentity',
            'lifestyleAndDailyRoutine',
            'valuesAndBeliefs'
        ]
        
        for category in categories:
            if category in user_profile:
                texts.extend(str(value) for value in user_profile[category].values() if value)
        
        return ' '.join(texts)
    
    def calculate_bert_embeddings(self):
        """计算BERT嵌入"""
        texts = [self.extract_character_text(char['profile']) for char in self.data]
        print("Calculating BERT embeddings...")
        return self.model.encode(texts)
    
    def visualize_similarity_tsne(self, embeddings, output_file='character_similarity_tsne.png'):
        """使用t-SNE可视化BERT嵌入"""
        # t-SNE降维
        tsne = TSNE(
            n_components=2,
            perplexity=3,
            random_state=42,
            init='random',
            learning_rate=200,
            n_iter=2000
        )
        embeddings_2d = tsne.fit_transform(embeddings)
        
        # 准备可视化数据
        names = [char['profile']['userProfile']['demographicInformation'].get('name', f'Character {i}') 
                for i, char in enumerate(self.data)]
        genders = [char['profile']['userProfile']['demographicInformation'].get('gender', 'Unknown') 
                  for char in self.data]
        
        # 创建图表
        plt.figure(figsize=(12, 8))
        
        # 设置颜色方案
        gender_colors = {
            'Male': '#4C72B0',     # 深蓝色
            'Female': '#DD8452',   # 珊瑚色
            'Unknown': '#937860'   # 棕色
        }
        
        # 绘制散点图
        for gender in set(genders):
            mask = [g == gender for g in genders]
            mask = np.array(mask)
            plt.scatter(
                embeddings_2d[mask, 0],
                embeddings_2d[mask, 1],
                c=[gender_colors.get(gender)],
                s=100,
                alpha=0.7,
                label=gender,
                edgecolors='white',
                linewidth=1
            )
        
        # 添加标签
        for i, (x, y) in enumerate(embeddings_2d):
            plt.annotate(
                names[i],
                (x, y),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=9,
                color='black',
                bbox=dict(
                    facecolor='white',
                    edgecolor='lightgray',
                    alpha=0.8,
                    boxstyle='round,pad=0.3'
                )
            )
        
        # 设置坐标轴
        plt.xlabel('t-SNE Dimension 1', fontsize=12)
        plt.ylabel('t-SNE Dimension 2', fontsize=12)
        
        # 设置标题和图例
        plt.title('Character Similarity Map (BERT + t-SNE)', fontsize=14, pad=20)
        plt.legend(
            title='Gender',
            frameon=True,
            fontsize=10,
            title_fontsize=11,
            loc='center left',
            bbox_to_anchor=(1, 0.5)
        )
        
        # 设置刻度字体大小
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        
        # 调整布局并保存
        plt.tight_layout()
        plt.savefig(
            output_file,
            dpi=300,
            bbox_inches='tight',
            facecolor='white',
            edgecolor='none'
        )
        plt.close()

def main():
    analyzer = CharacterAnalyzer('town_characters.json')
    embeddings = analyzer.calculate_bert_embeddings()
    analyzer.visualize_similarity_tsne(embeddings)
    print("Visualization saved as 'character_similarity_tsne.png'")

if __name__ == "__main__":
    main()