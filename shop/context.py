from . import cart
from .models import Category


def store(request):
    lines = cart.get_lines(request)
    return {"nav_categories": Category.objects.all(), "cart_count": sum(lines.values()), "free_from": cart.FREE_DELIVERY_FROM}
