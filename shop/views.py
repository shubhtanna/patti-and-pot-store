import json
import secrets

from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.http import require_POST

from . import cart
from .models import Category, Order, OrderItem, Product
from .templatetags.shop_extras import rupees


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
    jsonld = json.dumps(_product_jsonld(request, p)).replace("<", "\\u003c")
    return render(request, "shop/product.html", {"p": p, "related": related, "jsonld": jsonld,
                                                 "qty_range": range(1, min(5, max(p.stock, 1)) + 1)})


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
    try:
        qty = max(1, int(request.POST.get("qty") or 1))
    except ValueError:
        qty = 1
    cart.add(request, p, qty)
    messages.success(request, f"Added {p.name} to your cart.")
    return HttpResponseRedirect(request.headers.get("Referer") or reverse("cart"))


@require_POST
def cart_update(request):
    cart.set_qty(request, request.POST.get("sku", ""), int(request.POST.get("qty") or 0))
    return redirect("cart")


def cart_view(request):
    return render(request, "shop/cart.html", {"cart": cart.summary(request)})


FIELDS = ("name", "phone", "email", "address", "city", "pincode", "payment")


def checkout(request):
    # A shareable checkout link (?items=sku:qty,sku:qty) rebuilds the cart without cookies,
    # so the link an agent hands the shopper opens the same items on any device.
    items_param = request.GET.get("items", "")
    if items_param:
        cart.load_from_items(request, items_param)
        return redirect("checkout")
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
        "# Estate-direct teas from Assam, Darjeeling and the Nilgiris, packed fresh in Pune.",
        "User-agent: *",
        "Disallow: /cart/",
        "Disallow: /checkout/",
        "Disallow: /order/",
        "Allow: /",
        "Sitemap: /sitemap.xml",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/plain")


def _product_jsonld(request, p):
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": p.name,
        "description": p.description,
        "image": request.build_absolute_uri(static(f"img/tins/{p.slug}.svg")),
        "sku": p.sku,
        "url": request.build_absolute_uri(p.get_absolute_url()),
        "offers": {
            "@type": "Offer",
            "price": str(p.price),
            "priceCurrency": "INR",
            "availability": "https://schema.org/InStock" if p.stock else "https://schema.org/OutOfStock",
            "url": request.build_absolute_uri(p.get_absolute_url()),
        },
    }


def sitemap(request):
    urls = [request.build_absolute_uri(reverse("home"))]
    urls += [request.build_absolute_uri(c.get_absolute_url()) for c in Category.objects.all()]
    urls += [request.build_absolute_uri(p.get_absolute_url()) for p in Product.objects.all()]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"<url><loc>{u}</loc></url>" for u in urls]
    xml.append("</urlset>")
    return HttpResponse("\n".join(xml) + "\n", content_type="application/xml")


def llms(request):
    lines = [
        "# Patti & Pot",
        "Estate-direct Assam, Darjeeling and Nilgiri teas, masala chai blends and teaware,",
        "packed fresh in Pune and shipped across India.",
        "",
        "## Products",
    ]
    for p in Product.objects.all():
        lines.append(f"- [{p.name}]({p.get_absolute_url()}): {rupees(p.price)}")
    lines += [
        "",
        "## How to buy",
        "1. Open a product page and submit its Add to cart form (a plain HTML form; no JavaScript needed).",
        "2. Review the items at /cart/.",
        "3. Send the shopper the checkout link shown on the cart page, e.g. /checkout/?items=SKU:QTY,SKU:QTY.",
        "   It opens the same items on any device, no cookies required.",
        "4. The shopper fills in delivery details and pays by cash on delivery or UPI on delivery.",
    ]
    return HttpResponse("\n".join(lines) + "\n", content_type="text/markdown")


def not_found(request, exception=None):
    return render(request, "shop/404.html", status=404)
