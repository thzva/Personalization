from sentence_transformers import SentenceTransformer
import numpy as np
import json

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np


with open('hyr_cleaned.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
def get_embeddings(data):
    # Load model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Define weights for each category
    weights = [0.05, 0.05, 0.15, 0.10, 0.10, 0.10, 0.05, 0.15, 0.05, 0.15, 0.10, 0.05]
    
    # Categories in order matching weights
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
        name = person['name']
        category_embeddings = []
        
        # Get embedding for each category if it exists
        for category in categories:
            if category in person:
                text = str(person[category])
                embedding = model.encode(text)
                category_embeddings.append(embedding)
            else:
                # Use zero vector if category missing
                category_embeddings.append(np.zeros(model.get_sentence_embedding_dimension()))
                
        # Calculate weighted average
        category_embeddings = np.array(category_embeddings)
        weighted_embedding = np.average(category_embeddings, axis=0, weights=weights)
        
        person_embeddings[name] = weighted_embedding
        
    return person_embeddings

# Load and process data
# with open('hyr_cleaned.json', 'r') as f:
#     data = json.load(f)

def visualize_embeddings(embeddings):
   names = list(embeddings.keys())
   embedding_array = np.array(list(embeddings.values()))
   
   tsne = TSNE(n_components=2, random_state=42)
   embeddings_2d = tsne.fit_transform(embedding_array)
   
   plt.figure(figsize=(10, 8))
   colors = ['#FF6B6B', '#4ECDC4']  # Red and turquoise
   
   for i in range(len(names)):
       plt.scatter(embeddings_2d[i, 0], embeddings_2d[i, 1], 
                  c=colors[i], s=50)
       plt.annotate(names[i], (embeddings_2d[i, 0], embeddings_2d[i, 1]),
                   fontsize=5)
   
   plt.title('t-SNE Visualization of Person Embeddings')
   plt.xlabel('t-SNE 1')
   plt.ylabel('t-SNE 2')
   plt.savefig('tsne1.png', dpi=300, bbox_inches='tight')
   plt.close()
    
embeddings = get_embeddings(data)
visualize_embeddings(embeddings)