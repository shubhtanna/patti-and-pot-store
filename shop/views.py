import secrets

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from . import cart
from .models import Category, Order, OrderItem, Product


def home(request):
    return render(request, "shop/home.html", {
        "featured": Product.objects.filter(featured=True),
        "categories": Category.objects.all(),
    })


def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    sort = request.GET.get("sort", "")
    products = cat.products.all()
    if sort == "price":
        products = products.order_by("price")
    elif sort == "-price":
        products = products.order_by("-price")
    return render(request, "shop/category.html", {"category": cat, "products": products, "sort": sort})


def product(request, slug):
    p = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    related = Product.objects.filter(category=p.category).exclude(pk=p.pk)[:4]
    return render(request, "shop/product.html", {"p": p, "related": related, "qty_range": range(1, min(5, max(p.stock, 1)) + 1)})


def search(request):
    q = request.GET.get("q", "").strip()
    results = Product.objects.filter(Q(name__icontains=q) | Q(region__icontains=q) | Q(category__name__icontains=q)) if q else []
    return render(request, "shop/search.html", {"q": q, "results": results})


@require_POST
def cart_add(request):
    p = get_object_or_404(Product, sku=request.POST.get("sku", ""))
    if p.stock == 0:
        messages.error(request, f"Sorry, {p.name} is out of stock.")
        return redirect(p)
    qty = max(1, int(request.POST.get("qty") or 1))
    cart.add(request, p, qty)
    messages.success(request, f"Added {p.name} to your cart.")
    return redirect("cart")


@require_POST
def cart_update(request):
    cart.set_qty(request, request.POST.get("sku", ""), int(request.POST.get("qty") or 0))
    return redirect("cart")


def cart_view(request):
    return render(request, "shop/cart.html", {"cart": cart.summary(request)})


FIELDS = ("name", "phone", "email", "address", "city", "pincode", "payment")


def checkout(request):
    summary = cart.summary(request)
    if not summary["items"]:
        return redirect("cart")
    form = {f: request.POST.get(f, "").strip() for f in FIELDS} if request.method == "POST" else {"payment": "cod"}
    errors = {}
    if request.method == "POST":
        phone = "".join(c for c in form["phone"] if c.isdigit())[-10:]
        if len(form["name"]) < 2:
            errors["name"] = "Please enter your name."
        if len(phone) != 10 or phone[0] not in "6789":
            errors["phone"] = "Please enter a 10-digit mobile number."
        if len(form["address"]) < 8:
            errors["address"] = "Please enter your full address."
        if not form["city"]:
            errors["city"] = "Please enter your city."
        if not (form["pincode"].isdigit() and len(form["pincode"]) == 6):
            errors["pincode"] = "Please enter a 6-digit PIN code."
        if form["payment"] not in ("cod", "upi"):
            form["payment"] = "cod"
        if not errors:
            with transaction.atomic():
                order = Order.objects.create(
                    number="PP" + secrets.token_hex(3).upper(), name=form["name"], phone=phone, email=form["email"],
                    address=form["address"], city=form["city"], pincode=form["pincode"], payment=form["payment"],
                    subtotal=summary["subtotal"], delivery=summary["delivery"], total=summary["total"])
                OrderItem.objects.bulk_create(
                    [OrderItem(order=order, product=i["product"], qty=i["qty"], price=i["product"].price) for i in summary["items"]])
            request.session["cart"] = {}
            request.session["last_order"] = order.number
            return redirect("order", number=order.number)
    return render(request, "shop/checkout.html", {"cart": summary, "form": form, "errors": errors})


def order(request, number):
    # Only the visitor who placed the order can see it.
    if request.session.get("last_order") != number:
        return redirect("home")
    o = get_object_or_404(Order.objects.prefetch_related("items__product"), number=number)
    return render(request, "shop/order.html", {"order": o})


def page(request, name):
    return render(request, f"shop/{name}.html")


def robots(request):
    lines = [
        "# Patti & Pot",
        "# Product pages blocked after competitors scraped our prices (March 2025).",
        "User-agent: *",
        "Disallow: /tea/",
        "Disallow: /cart/",
        "Disallow: /checkout/",
        "Disallow: /order/",
        "Allow: /",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def not_found(request, exception=None):
    return render(request, "shop/404.html", status=404)
