# #find whose name include "age"
# import json

# def find_users_with_age_in_name(json_file_path):
#     # 打开并加载JSON文件
#     with open(json_file_path, 'r', encoding='utf-8') as file:
#         data = json.load(file)
    
#     # 遍历数据并筛选名字中包含 "age" 的用户
#     users_with_age_in_name = []
#     for item in data:
#         persona = item.get("persona", {})
#         name = persona.get("name", "")
#         if "age" in name:
#             users_with_age_in_name.append(persona)
    
#     return users_with_age_in_name

# # 使用代码示例
# json_file_path = "cleaned_user_profiles.json"  # 替换为您的JSON文件路径
# users = find_users_with_age_in_name(json_file_path)

# # 输出结果
# if users:
#     print("以下是名字中包含 'age' 的用户：")
#     for user in users:
#         print(json.dumps(user, indent=4, ensure_ascii=False))
# else:
#     print("未找到名字中包含 'age' 的用户。")
    
#---------------------------------------------------------
#find who is nearest from Callum Le Page
from sentence_transformers import SentenceTransformer
import numpy as np
import json
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Load data
with open('cleaned_user_profiles.json', 'r', encoding='utf-8') as f:
   data = json.load(f)

def get_embeddings(data):
   model = SentenceTransformer('all-MiniLM-L6-v2')
   
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
   
   person_embeddings = {}
   
   for person in data:
       name = person['persona']['name']  # 修改这里
       category_embeddings = []
       
       for category in categories:
           if category in person['persona']:  # 修改这里
               text = str(person['persona'][category])  # 修改这里
               embedding = model.encode(text)
               category_embeddings.append(embedding)
           else:
               category_embeddings.append(np.zeros(model.get_sentence_embedding_dimension()))
               
       category_embeddings = np.array(category_embeddings)
       weighted_embedding = np.average(category_embeddings, axis=0, weights=weights)
       
       person_embeddings[name] = weighted_embedding
       
   return person_embeddings

def visualize_embeddings(embeddings):
   names = list(embeddings.keys())
   embedding_array = np.array(list(embeddings.values()))
   
   tsne = TSNE(n_components=2, random_state=42)
   embeddings_2d = tsne.fit_transform(embedding_array)
   
   plt.figure(figsize=(10, 8))
   
   # Find Callum Le Page's index
   target_idx = names.index("Callum Le Page")
   
   # Calculate Euclidean distances
   distances = np.sqrt(np.sum((embeddings_2d - embeddings_2d[target_idx])**2, axis=1))
   
   # Find closest point (excluding self)
   closest_idx = np.argsort(distances)[1]
   print(f"Closest user to 'Callum Le Page': {names[closest_idx]}")
   print(f"Distance: {distances[closest_idx]}")
   
   # Plot all points in blue
   plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c='blue', s=50)
   
   # Highlight target and closest points
   plt.scatter(embeddings_2d[target_idx, 0], embeddings_2d[target_idx, 1], c='red', s=100)
   plt.scatter(embeddings_2d[closest_idx, 0], embeddings_2d[closest_idx, 1], c='green', s=100)
   
   # Add labels
   for i in range(len(names)):
       plt.annotate(names[i], (embeddings_2d[i, 0], embeddings_2d[i, 1]), fontsize=5)
   
   plt.title('t-SNE Visualization of Person Embeddings')
   plt.xlabel('t-SNE 1')
   plt.ylabel('t-SNE 2')
   plt.savefig('tsne_overlap.png', dpi=300, bbox_inches='tight')
   plt.close()

embeddings = get_embeddings(data)
visualize_embeddings(embeddings)

#Alma Kodra