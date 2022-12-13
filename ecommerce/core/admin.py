from django.contrib import admin

# Register your models here.
from .models import User
from ecom_api.models import Product, Cart

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)