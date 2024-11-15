import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import json

# Read JSON file
with open('cleaned.json', 'r') as f:
    data = json.load(f)

model = SentenceTransformer('all-MiniLM-L6-v2')

categories = ['demographic_information', 'physical_and_health_characteristics', 
              'psychological_and_cognitive_aspects', 'cultural_and_social_context',
              'relationships_and_social_networks', 'career_and_work_identity',
              'education_and_learning', 'hobbies_interests_and_lifestyle',
              'lifestyle_and_daily_routine', 'core_values_beliefs_and_philosophy',
              'emotional_and_relational_skills', 'media_consumption_and_engagement']

colors = plt.cm.rainbow(np.linspace(0, 1, len(categories)))
embeddings = []
labels = []

for person in data:
    for cat in categories:
        if cat in person and isinstance(person[cat], str):
            embedding = model.encode(person[cat])
            embeddings.append(embedding)
            labels.append(cat)

embeddings_array = np.array(embeddings)
tsne = TSNE(n_components=2, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings_array)

plt.figure(figsize=(10, 8))
for cat, color in zip(categories, colors):
    mask = [l == cat for l in labels]
    if any(mask):
        plt.scatter(embeddings_2d[mask, 0], embeddings_2d[mask, 1], 
                   color=color, label=cat)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('tsne_category.png', bbox_inches='tight')
plt.close()