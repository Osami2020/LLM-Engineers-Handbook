from abc import ABC
from typing import Optional

from pydantic import UUID4, Field

from .base import VectorBaseDocument
from .types import DataCategory


class CleanedDocument(VectorBaseDocument, ABC):
    content: str
    platform: str
    author_id: UUID4
    author_full_name: str


class CleanedPostDocument(CleanedDocument):
    image: Optional[str] = None

    class Config:
        name = "cleaned_posts"
        category = DataCategory.POSTS
        use_vector_index = False


class CleanedArticleDocument(CleanedDocument):
    link: str

    class Config:
        name = "cleaned_articles"
        category = DataCategory.ARTICLES
        use_vector_index = False


class CleanedRepositoryDocument(CleanedDocument):
    name: str
    link: str

    class Config:
        name = "cleaned_repositories"
        category = DataCategory.REPOSITORIES
        use_vector_index = False


class Chunk(VectorBaseDocument, ABC):
    content: str
    platform: str
    author_id: UUID4
    document_id: UUID4
    author_full_name: str
    metadata: dict = Field(default_factory=dict)


class EmbeddedChunk(VectorBaseDocument, ABC):
    content: str
    platform: str
    embedding: list[float] | None
    author_id: UUID4
    document_id: UUID4
    author_full_name: str
    metadata: dict = Field(default_factory=dict)


class DataCategory(StrEnum):
    POSTS = "posts"
    ARTICLES = "articles"
    REPOSITORIES = "repositories"
