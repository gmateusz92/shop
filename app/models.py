from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.conf import settings

CATEGORY_CHOICES = (# w template daje object.get_category_display
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)




class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField() #do get absolute potrzebne
    description = models.TextField()


    def __str__(self):
        return self.title

    def get_absolute_url(self):  # po to zeby bylo przkierowanie w template zamiast pk
        return reverse('app:product-page', kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse('app:add-to-cart', kwargs={'slug': self.slug})

    def remove_from_cart_url(self):
        return reverse('app:remove-from-cart', kwargs={'slug': self.slug})

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username