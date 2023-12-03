from django.contrib import admin
from .models import ShoppingCart, ShoppingCartItem

class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)

    actions = ['mark_as_completed']

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')

    mark_as_completed.short_description = "Seçili sepetleri tamamlandı olarak işaretle"

class ShoppingCartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'subtotal')
    list_filter = ('cart__status',)
    search_fields = ('cart__user__username', 'product__name')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(ShoppingCartItem, ShoppingCartItemAdmin)