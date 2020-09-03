import mptt
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.contrib.auth.models import Group
from django.db import models
from django.urls import reverse


class Category(MPTTModel):
    name = models.CharField(db_index=True,
                            max_length=200)

    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True,
                            related_name='children')

    slug = models.SlugField(unique=True,
                            max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_slug_list(self):
        try:
            ancestors = self.get_ancestors(include_self=True)
        except:
            ancestors = []
        else:
            ancestors = [i.slug for i in ancestors]

        slugs = []
        for i in range(len(ancestors)):
            slugs.append('/'.join(ancestors[:i+1]))
        return slugs

    @property
    def get_products(self):
        products = list()
        print(*self.get_children())
        for category in self.get_children():
            print('hi')
            products.append(Product.objects.filter(
                category__name=category.name))
        return products

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product', args=[str(self.slug)])

    def get_cat_list(self):
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent
        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = "/".join(breadcrumb[-1: i - 1: -1])
        return breadcrumb[-1:0:-1]
