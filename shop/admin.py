from django.contrib import admin
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'in_stock', 'updated_at')
    list_filter = ('in_stock', 'category', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ("product", "quantity", "price_at_purchase")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_email', 'created_at', 'total_items', 'total_amount')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'customer_email', 'id')
    inlines = [OrderItemInline]
    ordering = ('-created_at',)
