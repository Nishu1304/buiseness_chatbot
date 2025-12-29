from integrations.bos.factory import get_bos_client
from apps.llm.answer import generate_answer


def handle_purchase_history(client, phone: str) -> str:
    bos = get_bos_client()

    customer = bos.get_customer_by_phone(phone)
    if not customer:
        return (
            "I couldn’t find any purchase history for your number. "
            "Please ensure you used the same phone number at the store."
        )

    customer_id = customer["customer_id"]

    bills = bos.get_bills(customer_id)
    payments = bos.get_payments(customer_id)

    if not bills:
        return "You don’t have any purchase history yet."

    # Build structured context (VERY IMPORTANT)
    bill_lines = []
    total_spent = 0

    for bill in bills:
        total_spent += float(bill["grand_total"])
        items = ", ".join(
            [it["product_name"] for it in bill["items"]]
        )
        bill_lines.append(
            f"- {bill['date']} | ₹{bill['grand_total']} | Items: {items}"
        )

    payment_lines = [
        f"- {p['type']} ₹{p['amount']}"
        for p in payments
    ]

    context = f"""
Purchase history:
{chr(10).join(bill_lines)}

Payments:
{chr(10).join(payment_lines)}

Total spent: ₹{total_spent}
"""

    prompt = (
        "Summarize the user's purchase history clearly, in a paragraph format.\n"
        "Use ₹ for currency.\n"
        "No need to list every purchase. \n"
        "Do not invent values.\n"
        "Give them a brief overview of what was their highest or lowest purchases or if any pattern.\n"
        "Give the users some insights of their purchases if any or else None"
    )

    return generate_answer(context, prompt)
