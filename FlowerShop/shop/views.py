from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.db.models import Q
from .models import Product, Category


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = "product"


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    
    
    template_name = 'shop/product/list.html'

    def get_context_data(self, **kwargs):
        
        
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        return context

class ProductListByCategoryView(ListView):
    model = Product
    context_object_name = "products"
    template_name = 'shop/product/list.html'

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()

        return context

def show_category(request, hierarchy=None):
    if hierarchy is None:
        return reverse('shop:products')
    category_slug = hierarchy.split("/")
    parent = None
    root = Category.objects.all()
    categories = Category.objects.all()
    for slug in category_slug[:-1]:
        parent = root.get(parent=parent, slug=slug)

    try:
        instance = Category.objects.get(parent=parent, slug=category_slug[-1])
    except:
        instance = get_object_or_404(Product, slug=category_slug[-1])
        return render(
            request, "shop/product/detail.html", {"instance": instance,"categories": root} 
        )
    else:
        return render(request, "shop/product/categories.html", {"instance": instance,"categories": root}) 