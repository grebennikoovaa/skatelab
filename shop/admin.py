from django.contrib import admin
from .models import Category, Product, ProductGalleryImage, ProductSpecification


class ProductGalleryImageInline(admin.TabularInline):
    model = ProductGalleryImage
    extra = 4
    fields = ('sort_order', 'image', 'alt_text')


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 3
    fields = ('sort_order', 'text')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort_order', 'slug', 'product_count', 'is_active')
    list_editable = ('sort_order', 'product_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('sort_order', 'id')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sort_order',
        'brand',
        'category',
        'price',
        'level',
        'width',
        'is_active',
    )
    list_editable = ('sort_order', 'price', 'is_active')
    list_filter = ('category', 'brand', 'level', 'width', 'is_active')
    search_fields = ('brand', 'name', 'title', 'description')
    prepopulated_fields = {'slug': ('brand', 'name')}
    ordering = ('sort_order', 'id')
    inlines = [ProductGalleryImageInline, ProductSpecificationInline]


@admin.register(ProductGalleryImage)
class ProductGalleryImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'sort_order', 'alt_text')
    list_editable = ('sort_order',)
    search_fields = ('product__brand', 'product__name', 'alt_text')
    ordering = ('sort_order', 'id')


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'sort_order', 'text')
    list_editable = ('sort_order',)
    search_fields = ('product__brand', 'product__name', 'text')
    ordering = ('sort_order', 'id')