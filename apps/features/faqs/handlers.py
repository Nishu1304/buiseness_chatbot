from apps.rag.retriever import retrieve_context
from apps.llm.answer import generate_answer


def handle_faq(client, user_question: str) -> str:
    context_docs = retrieve_context(client.id, user_question)

    if not context_docs:
        return (
            "I’m not sure about that right now. "
            "Please contact the store for more details."
        )

    context = "\n\n".join(context_docs)

    return generate_answer(context, user_question)
