from apps.features.products.category import match_category, load_products_for_category
from apps.features.products.browse import show_next_batch
from apps.common.messages import ChatMessage


def handle_product_state(session, text):
    ctx = session.context

    if text.lower() == "category":
        session.context["mode"] = "CATEGORY_SELECT"
        session.save()
        return ChatMessage(text="Please choose a category.")

    if text.lower() == "more" and ctx.get("mode") == "PRODUCT_LIST":
        return show_next_batch(session)

    if ctx.get("mode") == "CATEGORY_SELECT":
        cat = match_category(text, ctx.get("categories", []))
        if not cat:
            return ChatMessage(text="Please select a valid category.")

        load_products_for_category(session, cat)
        return show_next_batch(session)

    return None
