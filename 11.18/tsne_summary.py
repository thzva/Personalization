from sentence_transformers import SentenceTransformer
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import json

with open('cleaned_summary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Extract summaries and names 
summaries = []
names = []
for item in data:
   try:
       summaries.append(item['summary'])
       names.append(item['name'])
   except KeyError:
       continue

# Calculate embeddings
embeddings = model.encode(summaries)

# Apply TSNE
tsne = TSNE(n_components=2, random_state=42)
embeddings_2d = tsne.fit_transform(embeddings)

# Plot
plt.figure(figsize=(10, 8))
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1])
for i, name in enumerate(names):
   plt.annotate(name, (embeddings_2d[i, 0], embeddings_2d[i, 1]))
plt.title('TSNE visualization of persona embeddings')
plt.savefig('embeddings_viz.png')
plt.close()