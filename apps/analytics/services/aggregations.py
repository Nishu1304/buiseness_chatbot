from collections import defaultdict
from decimal import Decimal


def aggregate_monthly_sales(bills):
    total_revenue = Decimal("0")
    total_bills = len(bills)

    product_sales = defaultdict(lambda: {
        "quantity": 0,
        "revenue": Decimal("0")
    })

    for bill in bills:
        total_revenue += Decimal(str(bill["grand_total"]))

        for item in bill.get("items", []):
            name = item["product_name"]
            qty = item["quantity"]
            subtotal = Decimal(str(item["subtotal"]))

            product_sales[name]["quantity"] += qty
            product_sales[name]["revenue"] += subtotal

    top_products = sorted(
        product_sales.items(),
        key=lambda x: x[1]["revenue"],
        reverse=True
    )[:3]

    return {
        "total_revenue": float(total_revenue),
        "total_bills": total_bills,
        "avg_bill_value": float(total_revenue / total_bills) if total_bills else 0,
        "top_products": [
            {
                "name": name,
                "quantity": data["quantity"],
                "revenue": float(data["revenue"]),
            }
            for name, data in top_products
        ],
    }


from apps.features.feedback.models import Feedback
from django.db.models import Avg, Count


def aggregate_feedback(client, start_date, end_date):
    qs = Feedback.objects.filter(
        client=client,
        created_at__date__range=(start_date, end_date),
    )

    return {
        "feedback_count": qs.count(),
        "avg_rating": round(qs.aggregate(avg=Avg("rating"))["avg"] or 0, 2),
    }
