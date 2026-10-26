from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from llm_engineering.domain.cleaned_documents import (
    CleanedArticleDocument,
    CleanedDocument,
    CleanedPostDocument,
    CleanedRepositoryDocument,
)
from llm_engineering.domain.documents import (
    ArticleDocument,
    Document,
    PostDocument,
    RepositoryDocument,
)

from .operations import clean_text


DocumentT= TypeVar("DocumentT", bound= Document)

CleanedDocumentT = TypeVar("CleanedDocumentT", bound=CleanedDocument)

class CleaningDataHandler(ABC, Generic[DocumentT, CleanedDocumentT]):
    @abstractmethod
    def clean(self, data_model: PostDocument)-> CleanedPostDocument:
        return CleanedPostDocument(
            id=data_model.id,
            content=clean_text(" #### ".join(data_model.content.values())),
            image= data_model.image,
            link = data_model.link,
            author_full_name=data_model.author_full_name,
            author_id=data_model.author_id,
            platform=data_model.platform
        )
class ArticleCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: ArticleDocument)->CleanedArticleDocument:
        valid_content = [content for content in data_model.content.values if content] 
        return CleanedArticleDocument(
            id=data_model.id,
            content=clean_text(" ### ".join(valid_content)),
            platform=data_model.platform,
            link= data_model.link,
            author_id= data_model.author_id,
            author_full_name= data_model.author_full_name
        )   

class RepositoryCleaningHandler(CleaningDataHandler):
    def clean(self, data_model: RepositoryDocument) ->CleanedRepositoryDocument:
        return CleanedRepositoryDocument(
        id=data_model.id, 
        content=clean_text(" #### ".join(data_model.content.values())),
         id=data_model.id,
                    content=clean_text(" #### ".join(data_model.content.values())),
                    link = data_model.link,
                    author_full_name=data_model.author_full_name,
                    author_id=data_model.author_id,
                    platform=data_model.platform ,
                    name= data_model.name,
                    id = data_model.id)