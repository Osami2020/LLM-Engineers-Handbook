from io import BytesIO
import requests
from PIL import Image
from sentence_transformers import SentenceTransformer

response = requests.get("https://github.com/PacktPublishing/LLM-Engineering/blob/main/images/crazy_cat.jpg?raw=true"
)

image = Image.open(BytesIO(response.content))

model = SentenceTransformer("clip-ViT-B-32")

img_emb = model.encode(image)
text_emb=model.encode(
    ["A crazy cat smiling.",
"A white and brown cat with a yellow bandana.",
"A man eating in the garden."]
)
print(text_emb.shape)


similarity_Scores = model.similarity(img_emb, text_emb)

print(similarity_Scores)
