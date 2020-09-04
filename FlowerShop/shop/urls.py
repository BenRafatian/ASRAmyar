from django.urls import path, re_path
from django.views.generic import TemplateView

from .views import ProductDetailView, ProductListView, show_category

app_name = "shop"

urlpatterns = [
    path("", TemplateView.as_view(template_name="shop/base.html")),
    re_path(r"^products/(?P<hierarchy>.+)/$", show_category, name="ProductListByCategory"),
    path("products/", ProductListView.as_view(), name="products"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product",),
    

]
