import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer

# Example dataset: 10 titles
titles = [
    "Deep Learning for Image Recognition",
    "Natural Language Processing with Transformers",
    "Data Structures and Algorithms in Python",
    "Introduction to Machine Learning",
    "Advanced Python Programming",
    "Big Data Analytics with Hadoop",
    "Neural Networks and Deep Learning",
    "Reinforcement Learning Explained",
    "Statistics for Data Science",
    "Computer Vision and Image Processing"
]

# Step 1: Convert titles to vectors using a simple embedding method
vectorizer = TfidfVectorizer()
title_vectors = vectorizer.fit_transform(titles).toarray().astype(np.float32)

# Step 2: Determine parameters for LSH
d = title_vectors.shape[1]  # Dimension of the vectors
n_bits = 8  # Number of bits for LSH (adjustable parameter)

# Step 3: Create and train the FAISS LSH index
index = faiss.IndexLSH(d, n_bits)

# Convert title_vectors to float32 (required by FAISS)
title_vectors = title_vectors.astype(np.float32)

# Add vectors to the index
index.add(title_vectors)

# Step 4: Perform approximate nearest neighbor search for each title
sorted_indices = []
for i in range(len(titles)):
    query_vector = title_vectors[i:i+1]  # Get the i-th vector as a query
    D, I = index.search(query_vector, len(titles))  # Retrieve all titles sorted by similarity
    sorted_indices.append(I[0])

# Step 5: Display titles sorted by similarity
print("Titles Sorted by Similarity (LSH):")
for i, idx in enumerate(sorted_indices):
    print(f"{i + 1}. {titles[i]}")
    print("   Similar Titles:")
    for j in idx:
        if j != i:  # Exclude self-similarity
            print(f"   - {titles[j]}")
    print()
