from django.db import models


def calc_cart(cart):
    cart_data = cart.product.aggregate(models.Sum('total_price'), models.Count('id'))
    print(cart_data )
    if cart_data.get('total_price__sum'):
        cart.total_price = cart_data['total_price__sum']
    else: 
        cart.total_price=0
    cart.total_products = cart_data['id__count']
    cart.save()