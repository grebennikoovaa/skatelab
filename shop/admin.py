from django.contrib import admin
from .models import Product, ProductGalleryImage, ProductSpecification, Favorite


class ProductGalleryImageInline(admin.TabularInline):
    model = ProductGalleryImage
    extra = 1


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'brand',
        'name',
        'price',
        'category',
    )

    search_fields = (
        'brand',
        'name',
        'description',
    )

    list_filter = (
        'category',
        'brand',
    )

    prepopulated_fields = {
        'slug': ('brand', 'name'),
    }

    inlines = [
        ProductGalleryImageInline,
        ProductSpecificationInline,
    ]


@admin.register(ProductGalleryImage)
class ProductGalleryImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'alt_text',
    )

    search_fields = (
        'product__brand',
        'product__name',
        'alt_text',
    )


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'product',
        'text',
    )

    search_fields = (
        'product__brand',
        'product__name',
        'text',
    )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'product',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'product__brand',
        'product__name',
    )

    list_filter = (
        'created_at',
    )