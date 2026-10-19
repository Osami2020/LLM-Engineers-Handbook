from llm_engineering.domain.documents import ArticleDocument, UserDocument

user = UserDocument.get_or_create(first_name="Paul", last_name="Iusztin")
articles = ArticleDocument.bulk_find(author_id=str(user.id))
print(f"User ID: {user.id}")
print(f"User name: {user.first_name} {user.last_name}")
print(f"Number of articles: {len(articles)}")
print("First article link:", articles[0].link)
