from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views


app_name = "shop"

urlpatterns = [
    path("", TemplateView.as_view(template_name="shop/base.html")),
    path('search/', views.SearchResultsView.as_view(), name="search_results"),
    re_path(r"^products/(?P<hierarchy>.+)/$",
            views.product_detail_or_list_by_category, name="ProductListByCategory"),
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/<slug:slug>/", views.ProductDetailView.as_view(), name="product",),


]
