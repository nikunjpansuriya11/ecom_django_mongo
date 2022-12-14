from ecom_api.models import  Product, Cart, Images, Sizes
from ecom_api.serializers.product_serializer import AllProductSerializer

def all_cart_product(user_id):
    if Cart.objects.filter(user = user_id).exists():
        all_cart_data = Cart.objects.get(user = user_id)
    else:
        all_cart_data = None
    return all_cart_data

def cart_data_serializer(cart_data):
    cart_productdata = list(cart_data.product_id)
    product_data = Product.objects.filter(product_id__in=cart_productdata)    
    cart_allproduct_data = AllProductSerializer(product_data,many=True)
    cart_json = {
        "cart_id":cart_data.cart_id,
        "Products":cart_allproduct_data.data,
    }
    return cart_json
