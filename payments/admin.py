from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'reference', 'amount', 'payment_method', 'verified', 'date_updated')
    list_filter = ('user', 'amount', 'payment_method', 'verified', 'date_updated')
    search_fields = ('user', 'reference')


admin.site.register(Payment, PaymentAdmin)
