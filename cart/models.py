from django.db import models
from product.models import Product
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

STATUS_CHOICES = [
    ('waiting', 'Bekleniyor'),
    ('buyed', 'Satın Alındı'),
    ('deleted', 'Silindi'),
]

class ShoppingCartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} - Fiyat: {self.price} TL"

class ShoppingCart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=32, blank=True, null=True)
    items = models.ManyToManyField(ShoppingCartItem, blank=True)
    total_price = models.FloatField(default=0)
    status = models.CharField(
        default="waiting", 
        choices=STATUS_CHOICES,
        max_length=10,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sipariş No: {self.pk} - Toplam: {self.total_price} - Durum: {self.status}"

    def total_price_update(self):
        if self.status == "waiting":
            total_price = self.items.filter(is_deleted=False).aggregate(total_price=models.Sum('price'))['total_price'] or 0
            self.total_price = total_price
            self.save()

@receiver(post_save, sender=ShoppingCartItem)
def shopping_cart_item_receiver(sender, instance, created, *args, **kwargs):
    if created:
        instance.price = instance.product.price
        instance.save()
    
    last_cart = instance.shoppingcart_set.last()
    if last_cart:
        last_cart.total_price_update()
    
    print(kwargs)
    print(f"{'x' * 30}\nShoppingCartItem\n{'x' * 30}")
    print(last_cart.total_price)

@receiver(m2m_changed, sender=ShoppingCart.items.through)
def shopping_cart_receiver(sender, instance, action, *args, **kwargs):
    if action in ['post_add', 'post_remove', 'post_clear']:
        instance.total_price_update()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(ShoppingCartItem)
    total_price = models.FloatField()
    shipping_address = models.TextField()
    payment_status = models.BooleanField(default=False)  # Ödeme durumu
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sipariş No: {self.pk} - Toplam: {self.total_price} - Ödeme: {self.payment_status}"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.FloatField()
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Kupon: {self.code} - İndirim: {self.discount_percentage}% - Son Kullanma: {self.expiration_date}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1-5 arasında bir değer
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} - Değerlendirme: {self.rating}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Favori Ürünler"

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.title} - İndirim: {self.discount_percentage}% - Başlangıç: {self.start_date} - Bitiş: {self.end_date}"
