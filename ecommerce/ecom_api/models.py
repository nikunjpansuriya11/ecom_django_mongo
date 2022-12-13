from djongo import models
from core.models import User
import uuid
from django import forms

class ScrapeProductUrl(models.Model):
    product_url_id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable= False)
    product_url = models.TextField(unique=True)
    product_type = models.CharField(max_length=255)
    is_scraped = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

class Sizes(models.Model):
    shoes_size = models.CharField(max_length=255)

    class Meta:
        abstract = True

class SizesForm(forms.ModelForm):
    class Meta:
        model = Sizes
        fields = ["shoes_size"]

class Images(models.Model):
    image_url = models.TextField()

    class Meta:
        abstract = True


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ["image_url"]

class Product(models.Model):
    product_id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable= False)
    product_url = models.TextField(unique=True)
    type = models.CharField(max_length=255)
    name = models.TextField()
    price = models.FloatField()
    dis_price = models.FloatField()
    color = models.CharField(max_length=255)
    size = models.ArrayField(model_container=Sizes, model_form_class=SizesForm)
    images = models.ArrayField(model_container=Images, model_form_class=ImagesForm)
    desc = models.JSONField(null=True,blank=True)
    desc_add = models.BooleanField(default=False)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)


class Cart(models.Model):
    cart_id = models.UUIDField(primary_key=True , default=uuid.uuid4 , editable= False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    product = models.ArrayReferenceField(
        to=Product,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
