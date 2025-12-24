"""Embedding model loader for ChatGIT"""

from langchain_community.embeddings import HuggingFaceBgeEmbeddings


def load_embedding_model(
    model_name: str = "BAAI/bge-large-en-v1.5", device: str = "cpu"
) -> HuggingFaceBgeEmbeddings:
    """Load embedding model for vector search
    
    Args:
        model_name: HuggingFace model identifier
        device: Device to run model on ('cpu' or 'cuda')
    
    Returns:
        Initialized embedding model
    """
    model_kwargs = {"device": device}
    encode_kwargs = {"normalize_embeddings": True}
    embedding_model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    return embedding_model
