from django.urls import include, path

urlpatterns = [path("", include("shop.urls"))]
handler404 = "shop.views.not_found"
