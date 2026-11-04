"""Admin configuration for the Store app."""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Brand, Product, ProductImage, ProductSpecification,
    Cart, CartItem, Order, OrderItem, ShippingAddress, Review, Wishlist
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'created_at']
    list_filter = ['parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary']


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 3
    fields = ['key', 'value']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'stock', 'is_available', 'created_at']
    list_filter = ['brand', 'category', 'is_available', 'vram', 'memory_type']
    search_fields = ['name', 'description', 'brand__name']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'stock', 'is_available']
    inlines = [ProductImageInline, ProductSpecificationInline]

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'brand', 'category', 'description')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'stock', 'is_available')
        }),
        ('Specifications', {
            'fields': ('vram', 'gpu_series', 'memory_type', 'interfaces', 'power_requirements', 'length', 'release_year')
        }),
    )


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'item_count']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__email']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total', 'is_demo', 'created_at']
    list_filter = ['status', 'is_demo', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'subtotal', 'tax', 'shipping', 'total', 'is_demo', 'created_at']
    list_editable = ['status']


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'user', 'city', 'state', 'country', 'is_default']
    list_filter = ['country', 'is_default']
    search_fields = ['full_name', 'user__username', 'city']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'title', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username', 'title', 'comment']
    list_editable = ['is_approved']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_count', 'created_at']
    filter_horizontal = ['products']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'