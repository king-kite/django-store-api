from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import CartItem, Order


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'ordered', 'date_updated']
    list_filter = ['user', 'product', 'quantity', 'ordered', 'date_updated']
    search_fields = ['user', 'product', 'quantity', 'ordered', 'date_updated']

    actions = ['mark_ordered', 'mark_unordered']

    def mark_ordered(self, request, queryset):
        updated = queryset.update(ordered=True)
        self.message_user(request, ngettext(
            '%d cart item was successfully marked as Ordered.',
            '%d cart items were successfully marked as Ordered.',
            updated,
            ) % updated, messages.SUCCESS)
    mark_ordered.allowed_permissions = ('change',)
    mark_ordered.short_description = "Mark selected orders as Ordered"

    def mark_unordered(self, request, queryset):
        updated = queryset.update(ordered=False)
        self.message_user(request, ngettext(
            '%d cart item was successfully marked as Unordered.',
            '%d cart items were successfully marked as Unordered.',
            updated,
            ) % updated, messages.SUCCESS)
    mark_unordered.allowed_permissions = ('change',)
    mark_unordered.short_description = "Mark selected orders as Unordered"


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ordered', 'status']
    list_display_links = ['id', 'user']
    list_filter = ['ordered', 'status']
    search_fields = ['user__username']

    actions = ['mark_ordered', 'mark_unordered', 'mark_being_delivered', 'mark_delivered']


    def mark_ordered(self, request, queryset):
        updated = queryset.update(ordered=True)
        self.message_user(request, ngettext(
            '%d order was successfully marked as Ordered.',
            '%d orders were successfully marked as Ordered.',
            updated,
            ) % updated, messages.SUCCESS)
    mark_ordered.allowed_permissions = ('change',)
    mark_ordered.short_description = "Mark selected orders as Ordered"

    def mark_unordered(self, request, queryset):
        updated = queryset.update(ordered=False)
        self.message_user(request, ngettext(
            '%d order was successfully marked as Unordered.',
            '%d orders were successfully marked as Unordered.',
            updated,
            ) % updated, messages.SUCCESS)
    mark_unordered.allowed_permissions = ('change',)
    mark_unordered.short_description = "Mark selected orders as Unordered"

    def mark_being_delivered(self, request, queryset):
        updated = queryset.update(status='BD')
        self.message_user(request, ngettext(
            '%d order was successfully marked as Being Delivered',
            '%d orders were successfully marked as Being Delivered',
            updated,
            ) % updated, messages.SUCCESS)
        for obj in queryset:
            obj.save()
    mark_being_delivered.allowed_permissions = ('change',)
    mark_being_delivered.short_description = "Mark selected orders as Being Delivered"

    def mark_delivered(self, request, queryset):
        updated = queryset.update(status='D')
        self.message_user(request, ngettext(
            '%d order was successfully marked as Delivered',
            '%d orders were successfully marked as Delivered',
            updated,
            ) % updated, messages.SUCCESS)
        for obj in queryset:
            obj.save()
    mark_delivered.allowed_permissions = ('change',)
    mark_delivered.short_description = "Mark selected orders as Delivered"


admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
