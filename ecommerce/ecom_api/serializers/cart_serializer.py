from rest_framework import serializers
from ecom_api.models import Product, Sizes, Images, Cart



class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ('cart_id', 'product_id')


    def validate_product(self, data):
        product_id = data['product_id']
        try:
            data = Product.objects.get(product_id=product_id)
        except Exception as e:
            return False
        return data


    def create(self, validated_data):
        if Cart.objects.filter(user=validated_data['user_id']).exists():
            cart = Cart.objects.get(user_id=validated_data['user_id'])
            cart.product.add(validated_data['product_id'])
            cart.save()
            return True
        else:
            cart = Cart.objects.create(user=validated_data['user_id'])
            cart.product.add(validated_data['product_id'])
            cart.save()
            return True

    def delete(self, validated_data):
        if Cart.objects.filter(user=validated_data['user_id']).exists():
            cart = Cart.objects.get(user_id=validated_data['user_id'])
            cart.product.remove(validated_data['product_id'])
            cart.save()
            return True
        else:
            return False

