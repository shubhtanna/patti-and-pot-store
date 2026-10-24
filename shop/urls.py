from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/<slug:slug>/", views.category, name="category"),
    path("tea/<slug:slug>/", views.product, name="product"),
    path("search/", views.search, name="search"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/", views.cart_add, name="cart_add"),
    path("cart/update/", views.cart_update, name="cart_update"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<str:number>/", views.order, name="order"),
    path("about/", views.page, {"name": "about"}, name="about"),
    path("shipping/", views.page, {"name": "shipping"}, name="shipping"),
    path("robots.txt", views.robots, name="robots"),
]
