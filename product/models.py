from django.db import models
from page.models import DEFAULT_STATUS, STATUS
from django.contrib.auth.models import User

GENDER_CHOICE = [
    ('men', 'Erkek'),
    ('women', 'Kadin'),
    ('unisex', 'UniSex'),
]

class Category(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default="")
    status = models.CharField(default=DEFAULT_STATUS, choices=STATUS, max_length=10)
    gender = models.CharField(max_length=6, default="unisex", choices=GENDER_CHOICE)
    createt_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{1000 + self.pk } - {self.gender} - {self.title}"

class Image(models.Model):
    image = models.ImageField(upload_to='product_images/')

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, default="")
    content = models.TextField() 
    cover_image = models.ImageField(upload_to='page', null=True, blank=True)
    price = models.FloatField()
    stock = models.PositiveSmallIntegerField(default=0)
    is_home = models.BooleanField(default=False)
    status = models.CharField(default=DEFAULT_STATUS, choices=STATUS, max_length=10)
    createt_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    images = models.ManyToManyField(Image, blank=True)
    discounts = models.ManyToManyField('Discount', blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # 1-5 arasında bir değer
    comment = models.TextField()
