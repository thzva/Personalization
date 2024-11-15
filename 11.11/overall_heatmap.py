import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from tqdm import tqdm

def read_similarity_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_unique_names(similarity_data):
    all_names = set()
    for category in similarity_data:
        for entry in similarity_data[category]:
            all_names.add(entry['person1'])
            all_names.add(entry['person2'])
    return sorted(list(all_names))

def create_weighted_matrix(similarity_data, names, weights, categories):
    n = len(names)
    weighted_matrix = np.zeros((n, n))
    weight_sum = np.sum(weights)
    name_to_idx = {name: i for i, name in enumerate(names)}
    
    for category, weight in zip(categories, weights):
        matrix = np.ones((n, n))
        for entry in similarity_data[category]:
            if entry['similarity'] != "NAN":
                i = name_to_idx[entry['person1']]
                j = name_to_idx[entry['person2']]
                matrix[i, j] = entry['similarity']
                matrix[j, i] = entry['similarity']
        weighted_matrix += (matrix * weight)
    
    return weighted_matrix / weight_sum

def plot_weighted_heatmap(similarity_data, all_names, weights, categories):
    plt.figure(figsize=(12, 10))
    plt.rcParams.update({'font.size': 8})
    
    weighted_matrix = create_weighted_matrix(similarity_data, all_names, weights, categories)
    sns.heatmap(
        weighted_matrix,
        xticklabels=all_names,
        yticklabels=all_names,
        cmap='coolwarm',
        vmin=0,
        vmax=1,
        square=True,
        cbar_kws={
            'label': 'Weighted Similarity Score',
            'shrink': 0.8,
            'aspect': 20,
            'pad': 0.02
        }
    )
    
    # 设置较小的刻度标签字体
    plt.tick_params(axis='both', which='major', labelsize=6)
    
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.title('Weighted Similarity', pad=20, fontsize=10)
    
    plt.tight_layout()
    plt.savefig('weighted_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    weights = [0.05, 0.05, 0.15, 0.10, 0.10, 0.10, 0.05, 0.15, 0.05, 0.15, 0.10, 0.05]
    categories = [
        'demographic_information',
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
    
    similarity_data = read_similarity_data('similarity.json')
    all_names = get_unique_names(similarity_data)
    plot_weighted_heatmap(similarity_data, all_names, weights, categories)
    print("Heatmap saved as weighted_heatmap.png")

if __name__ == "__main__":
    main()