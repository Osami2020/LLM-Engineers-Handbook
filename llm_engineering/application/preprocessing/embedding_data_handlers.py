from abc import ABC, abstractmethod
from typing import Generic, TypeVar, cast

from llm_engineering.application.networks import EmbeddingModelSingleton
from llm_engineering.domain.chunks import ArticleChunk, Chunk, PostChunk, RepositoryChunk
from llm_engineering.domain.embedded_chunks import (
    EmbeddedArticleChunk,
    EmbeddedChunk,
    EmbeddedPostChunk,
    EmbeddedRepositoryChunk,
)
from llm_engineering.domain.queries import EmbeddedQuery, Query
ChunkT= TypeVar("ChunkT", bound=Chunk)
EmbeddedChunkT= TypeVar("EmbeddedChunkT", bound=EmbeddedChunk)

embedding_model = EmbeddingModelSingleton()

class EmbeddingDataHandler(ABC, Generic[ChunkT, EmbeddedChunkT]):
    """
    Abstract Class for all embedding data handlers.
    ALl data transformations logic for the embedding step is done here."""


    def embed(self, data_model: ChunkT)-> EmbeddedChunkT:
        return self.embed_batch([data_model])[0]

    def embed_batch(self, data_model: list[ChunkT])->list[EmbeddedChunkT]:
        embedding_model_input = [data]