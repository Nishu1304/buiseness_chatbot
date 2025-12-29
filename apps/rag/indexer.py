import os
import faiss
import numpy as np
from django.conf import settings
from apps.rag.models import RAGDocument
from apps.llm.embedding import embed_texts

INDEX_DIR = os.path.join(settings.BASE_DIR, "apps", "rag", "stores")
EMBED_DIM = 384  # MiniLM dimension


def build_client_index(client_id: int):
    os.makedirs(INDEX_DIR, exist_ok=True)

    docs = RAGDocument.objects.filter(
        client_id=client_id,
        is_active=True
    ).order_by("id")

    if not docs.exists():
        return None

    texts = [doc.content for doc in docs]
    embeddings = embed_texts(texts)

    vectors = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatIP(EMBED_DIM)  # cosine similarity
    index.add(vectors)

    index_path = os.path.join(INDEX_DIR, f"client_{client_id}.index")
    faiss.write_index(index, index_path)

    return index_path
