from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Product

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        'pk',
        'title',
        'slug',
        'gender',
        'status', 
        'updated_at',
    )
    list_filter = ('status', 'gender', )
    list_editable = (
        'title',
        'status', 
    )

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        'pk',
        'title',
        'cover_image',
        'price',
        'stock',
        'slug',
        'is_home',
        'status', 
        'updated_at',
        'category_link',  # category_link'i listeye ekledik
        'stock_status',  # stock_status'u listeye ekledik
    )
    list_filter = ('status', )
    list_editable = (
        'title',
        'is_home',
        'status', 
    )

    def category_link(self, obj):
        return format_html('<a href="{}">{}</a>', reverse('admin:yourapp_category_change', args=[obj.category.pk]), obj.category.title)

    category_link.short_description = 'Kategori'  # Kolon başlığını değiştirir

    actions = ['make_published']

    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='published')
        if rows_updated == 1:
            message_bit = "1 ürün"
        else:
            message_bit = f"{rows_updated} ürün"
        self.message_user(request, f"{message_bit} başarıyla yayınlandı.")

    make_published.short_description = "Seçili ürünleri yayınla"

    def stock_status(self, obj):
        if obj.stock > 0:
            return 'Stokta Var'
        else:
            return 'Stokta Yok'

    stock_status.short_description = 'Stok Durumu'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
