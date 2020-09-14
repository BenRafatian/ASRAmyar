from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin

from .models import Product, Category


admin.site.register(Category,
                    DraggableMPTTAdmin,
                    prepopulated_fields={"slug": ("name", )},
                    mptt_level_indent=60)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price",
                    "created", "updated", "available"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "available"]

    def get_prepopulated_fields(self, request, obj=None):
        return {"slug": {"name"}}
