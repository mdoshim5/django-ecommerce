from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
      return self.name

class Sub_Category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

    def __str__(self):
      return self.name


class Contact_us(models.Model):
    name= models.CharField(max_length=100)
    email=  models.CharField(max_length=100)
    subject= models.CharField(max_length=100)
    message= models.TextField()

    def __str__(self):
        return self.email

class Brand(models.Model):
    name = models.CharField(max_length= 150)


    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category, on_delete = models.CASCADE )
    brand = models.ForeignKey(Brand, on_delete = models.CASCADE, null = True)
    image = models.ImageField(upload_to = 'ecommerce/pimg')
    name = models.CharField(max_length= 100)
    price = models.IntegerField()
    date = models.DateField(auto_now_add = True)
    stock = models.IntegerField(default=0)


    def __str__(self):
      return self.name


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required = True, label ='Email', error_messages={'exists': 'This Email Already Exists'})

    class Meta:
        model = User
        fields =('username', 'first_name','last_name','email', 'password1','password2')

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

    def save(self, commit =True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']

class Order(models.Model):
    image = models.ImageField(upload_to='ecommerce/order/image')
    product = models.CharField(max_length = 1000, default='')
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    price = models.IntegerField()
    quantity = models.CharField(max_length= 5)
    total = models.CharField(max_length=1000, default='')
    address = models.TextField()
    phone = models.CharField(max_length= 10)
    pincode= models.CharField(max_length= 10)

    date = models.DateField(default = datetime.datetime.today)

    def __str__(self):
        return self.product

class PaymentRequest(models.Model):

    phone_number = models.CharField(max_length=20)
    name = models.CharField(max_length=255, default='test name')
    address = models.CharField(max_length=255)
    email = models.EmailField()
    product = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    pin = models.CharField(max_length=4)
    is_confirmed = models.BooleanField(default=False)
    list_display = ('address', 'email', 'product')

    def confirm_payment(self, request, queryset):
        # Process the payment confirmation logic
        # Set the payment status as confirmed and any other necessary updates

        # Redirect to the payment success page
        return redirect(reverse('payment_success'))

    confirm_payment.short_description = 'Confirm Payment'

    # Register the custom action in the admin panel
    actions = [confirm_payment]


