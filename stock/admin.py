from django.contrib import admin
from .models import *



admin.site.register(Product)

admin.site.register(Order)

admin.site.register(OrderItem)

admin.site.register(Client)
admin.site.register(Payment)


# Register your models here.
