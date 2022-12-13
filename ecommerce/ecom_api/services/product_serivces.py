from ecom_api.models import Product

def get_all_product():
    all_product = Product.objects.all()
    return all_product

