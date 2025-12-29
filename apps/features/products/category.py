from integrations.bos.factory import get_bos_client


def match_category(text, categories):
    print("DEBUG: user input =", text)
    print("DEBUG: available categories =", categories)

    text = text.lower()
    for idx, cat in enumerate(categories):
        print("DEBUG: checking category =", cat)

        if text == str(idx + 1):
            print("DEBUG: matched by number")
            return cat

        if cat["name"].lower() in text:
            print("DEBUG: matched by name")
            return cat

    print("DEBUG: no category matched")
    return None

def load_products_for_category(session, category):
    bos = get_bos_client()

    print("DEBUG: category selected =", category)
    print("DEBUG: category_id used =", category.get("category_id"))

    products = bos.get_products(category_id=category["category_id"])

    print("DEBUG: products returned =", products)
    # Prefer products with images
    products_with_images = []
    products_without_images = []

    for p in products:
        images = bos.get_product_images(p["product_id"])
        if images:
            p["_image"] = images[0]["image"]
            products_with_images.append(p)
        else:
            products_without_images.append(p)

    ordered = products_with_images + products_without_images

    session.context = {
        "mode": "PRODUCT_LIST",
        "category": category,
        "products": ordered,
        "offset": 0,
    }
    session.save()

    return ordered
