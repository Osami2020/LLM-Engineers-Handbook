from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLm-L6-v2")

sentences = [
    "The dog sits outside waiting for a treat.",
    "I am going swimming.",
    "The dog is swimming."
]

embeddings = model.encode(sentences)
print(embeddings.shape)

similarities = model.similarity(embeddings, embeddings)
print(similarities)