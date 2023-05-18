from django.contrib import admin

# Register your models here.
from .models import Category, Sub_Category, Product, Order, Contact_us, Brand
from .models import PaymentRequest
from django.shortcuts import redirect
from django.urls import reverse

admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Product)
admin.site.register(Contact_us)
admin.site.register(Order)
admin.site.register(Brand)

admin.site.register(PaymentRequest)


