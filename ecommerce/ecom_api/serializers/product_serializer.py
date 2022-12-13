from rest_framework import serializers
from ecom_api.models import Product, Sizes, Images
import uuid

class AllProductSerializer(serializers.ModelSerializer):
    size = serializers.JSONField()
    images = serializers.JSONField()
    desc = serializers.JSONField()
    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
