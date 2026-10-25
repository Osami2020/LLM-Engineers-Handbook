from typing_extensions import Annotated
from zenml import get_step_context, step

from llm_engineering.application.preprocessing import CleaningDispatcher
from llm_engineering.domain.cleaned_documents import CleanedDocument
from llm_engineering.application.preprocessing import ChunkingDispatcher
from llm_engineering.model import utils

@step
def clean_documents(
    documents: Annotated[ list, "raw_documents"],
)-> Annotated[list, "cleaned_documents"]:
    cleaned_documents = []
    for document in documents:

        cleaned_document = CleaningDispatcher.dispatch(document)
        cleaned_documents.append(cleaned_document)

    step_context = get_step_context()
    step_context.add_output_metadata(output_name= "cleaned_documents", metadata=_get_metadata(cleaned_documents))

    return cleaned_documents

@step
def chunk_and_embed(
    cleaned_documents: Annotated[list, "cleaned_documents"]
)-> Annotated[list, "embedded_documents"]:
    metadata = {"chunking": {}, "embedding": {}, "num_documents": len(cleaned_documents)}

    embedded_chunks = []
    for document in cleaned_documents:
        chunks= ChunkingDispatcher.dispatch(document)
        metadata["chunking"] = _add_chunks_metadata(chunks, metadata["chunking"])

        for batched_chaunks in utils.misc.batch(chunks, 10):
            embedded_chunks.extend(batched_embedded_chunks)

    metadata["embedding"] = _add_embeddings_metadata(embedded_chunks, metadata["embedding"])

    metadata["num_chunks"]=len(embedded_chunks)
    metadata["num_embedded_chunks"]= len(embedded_chunks)

    step_context= get_step_context()
    step_context.add_output_metadata(output_name="embedded documents", metadata=metadata)


    return embedded_chunks