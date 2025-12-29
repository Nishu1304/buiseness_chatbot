from apps.common.messages import ChatMessage


def show_next_batch(session):
    ctx = session.context
    products = ctx["products"]
    if not products:
        return ChatMessage(
            text="No products found in this category.\n"
                 "Type *category* to choose another or *menu* to go back."
        )
    offset = ctx["offset"]

    batch = products[offset: offset + 3]
    messages = []

    for p in batch:
        print(p)
        caption = (
            f"🛍️ {p['name']}\n"
            f"Brand: {p.get('brand') or '—'}\n"
            f"Price: ₹{p['selling_price']}"
        )

        if p.get("_image"):
            messages.append(
                ChatMessage(
                    image_url="https://images.unsplash.com/photo-1542291026-7eec264c27ff?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D", #p["_image"],
                    caption=caption
                )
            )
        else:
            messages.append(ChatMessage(text=caption))

    ctx["offset"] += 3
    session.context = ctx
    session.save()

    # Control message
    if ctx["offset"] < len(products):
        messages.append(ChatMessage(
            text="Reply *more* to see more products\n"
                 "Reply *category* to choose another category\n"
                 "Reply *menu* to go back"
        ))
    else:
        messages.append(ChatMessage(
            text="That’s all in this category 😊\n"
                 "Type *category* or *menu*."
        ))
    print(messages)
    return messages
