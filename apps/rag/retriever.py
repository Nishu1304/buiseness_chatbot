import os
import faiss
import numpy as np
from django.conf import settings
from apps.llm.embedding import embed_texts
from apps.rag.models import RAGDocument

INDEX_DIR = os.path.join(settings.BASE_DIR, "apps", "rag", "stores")
TOP_K = 3
EMBED_DIM = 384


def retrieve_context(client_id: int, query: str) -> list[str]:
    """
    Returns top-k relevant document contents for a client.
    """
    index_path = os.path.join(INDEX_DIR, f"client_{client_id}.index")

    if not os.path.exists(index_path):
        return []

    index = faiss.read_index(index_path)

    query_vec = embed_texts([query])
    query_np = np.array(query_vec).astype("float32")

    scores, indices = index.search(query_np, TOP_K)

    doc_ids = indices[0].tolist()

    # Fetch documents in the same order
    docs = (
        RAGDocument.objects
        .filter(client_id=client_id, is_active=True)
        .order_by("id")
    )

    contents = []
    for idx in doc_ids:
        if idx < docs.count():
            contents.append(docs[idx].content)

    return contents
