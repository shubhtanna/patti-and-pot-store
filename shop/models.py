from django.db import models
from django.urls import reverse


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=60)
    blurb = models.CharField(max_length=160)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", args=[self.slug])


class Product(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=120)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    region = models.CharField(max_length=80, blank=True)
    weight = models.CharField(max_length=40)
    price = models.PositiveIntegerField(help_text="INR, inclusive of GST")
    mrp = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    tasting_notes = models.CharField(max_length=160, blank=True)
    brew = models.CharField(max_length=160, blank=True)
    description = models.TextField()
    colour = models.CharField(max_length=7, help_text="Tin/label colour for the product art")
    featured = models.BooleanField(default=False)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["category__position", "position"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product", args=[self.slug])

    @property
    def percent_off(self):
        return round((1 - self.price / self.mrp) * 100) if self.mrp > self.price else 0


class Order(models.Model):
    number = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=80)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=60)
    pincode = models.CharField(max_length=6)
    payment = models.CharField(max_length=10, choices=[("cod", "Cash on delivery"), ("upi", "UPI on delivery")])
    subtotal = models.PositiveIntegerField()
    delivery = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveSmallIntegerField()
    price = models.PositiveIntegerField()
