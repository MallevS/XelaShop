from django.contrib import admin
from .models import *


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_total_price', 'gender', 'quantity', 'size']
    list_filter = ['gender', 'category__gender', 'season']
    search_fields = ['name']

    def display_total_price(self, obj):
        return f"${obj.price}"

    display_total_price.short_description = 'Product Price'

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(Product, ProductAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'display_total_amount', 'created_at', 'status', 'payment_method', 'shipping_method',
                    'order_number', 'shipping_address']
    actions = ['mark_as_pending', 'mark_as_sent', 'mark_as_delivered']

    def display_total_amount(self, obj):
        return f"${obj.total_amount}"

    display_total_amount.short_description = 'Total Price'

    def mark_as_pending(self, request, queryset):
        queryset.update(status='Pending')

    def mark_as_sent(self, request, queryset):
        queryset.update(status='Sent')

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='Delivered')

    mark_as_pending.short_description = "Mark selected orders as Pending"
    mark_as_sent.short_description = "Mark selected orders as Sent"
    mark_as_delivered.short_description = "Mark selected orders as Delivered"


admin.site.register(Order, OrderAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', ]


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', ]


admin.site.register(CartItem, CartItemAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'gender', 'parent_category']
    list_filter = ['gender']
    search_fields = ['name']


admin.site.register(Category, CategoryAdmin)


class MenProductAdmin(ProductAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(gender='M')


admin.site.register(MenProduct, MenProductAdmin)


class WomenProductAdmin(ProductAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(gender='F')


admin.site.register(WomenProduct, WomenProductAdmin)


class ImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Image, ImageAdmin)
