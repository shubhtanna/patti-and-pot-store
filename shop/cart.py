"""The cart, kept in the visitor's session."""

from .models import Product

FREE_DELIVERY_FROM = 699
DELIVERY_FEE = 79
MAX_QTY = 10


def get_lines(request):
    return dict(request.session.get("cart", {}))


def save_lines(request, lines):
    request.session["cart"] = {sku: qty for sku, qty in lines.items() if qty > 0}


def add(request, product, qty=1):
    lines = get_lines(request)
    lines[product.sku] = min(MAX_QTY, product.stock, lines.get(product.sku, 0) + qty)
    save_lines(request, lines)


def set_qty(request, sku, qty):
    lines = get_lines(request)
    lines[sku] = max(0, min(MAX_QTY, qty))
    save_lines(request, lines)


def load_from_items(request, items_param):
    """Rebuild the cart from a shareable checkout link: sku:qty,sku:qty."""
    lines = get_lines(request)
    for part in items_param.split(","):
        sku, _, qty = part.strip().partition(":")
        try:
            qty = int(qty)
        except ValueError:
            qty = 1
        p = Product.objects.filter(sku=sku).first()
        if p and qty > 0:
            lines[p.sku] = min(MAX_QTY, p.stock, lines.get(p.sku, 0) + qty)
    save_lines(request, lines)


def summary(request):
    lines = get_lines(request)
    products = {p.sku: p for p in Product.objects.filter(sku__in=lines.keys())}
    items = [{"product": products[sku], "qty": qty, "total": products[sku].price * qty} for sku, qty in lines.items() if sku in products]
    subtotal = sum(i["total"] for i in items)
    delivery = 0 if not items or subtotal >= FREE_DELIVERY_FROM else DELIVERY_FEE
    return {"items": items, "count": sum(i["qty"] for i in items), "subtotal": subtotal, "delivery": delivery,
            "total": subtotal + delivery, "free_from": FREE_DELIVERY_FROM, "to_free": max(0, FREE_DELIVERY_FROM - subtotal)}
