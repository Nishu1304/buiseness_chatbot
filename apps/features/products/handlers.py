from integrations.bos.factory import get_bos_client
from apps.common.messages import ChatMessage


BATCH_SIZE = 3


def start_product_catalog(session, client):
    bos = get_bos_client()
    categories = bos.get_categories()

    if not categories:
        return ChatMessage(text="No products available right now.")

    session.state = "PRODUCT_BROWSE"
    session.context = {
        "mode": "CATEGORY_SELECT",
        "categories": categories,
    }
    session.save()

    lines = ["🛍️ Product Categories:\n"]
    for idx, cat in enumerate(categories, start=1):
        lines.append(f"{idx}️⃣ {cat['name']}")

    lines.append("\nReply with a number or type the category name.")
    return ChatMessage(text="\n".join(lines))
