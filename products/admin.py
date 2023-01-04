from django.contrib import admin
from .models import Product, ProductImage, Review


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    min_num = 1
    max_num = 10
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'date_updated')
    list_filter = ('title', 'price', 'date_added')
    inlines = [
        ProductImageInline
    ]
    search_fields = ('title',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'rating', 'date_updated')
    list_filter = ('author', 'product', 'rating', 'date_updated')
    search_fields = ('author', 'product')


admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
