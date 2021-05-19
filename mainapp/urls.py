from .views import BaseView, ProductDetailView, CategoryDetailView, CartView, AddToCartView, DeleteFromCartView, ChangeCountView, OrderView, MakeOrderView
from django.urls import path

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/',ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name ='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-count/<str:ct_model>/<str:slug>/', ChangeCountView.as_view(), name='change_count'),
    path('order/', OrderView.as_view(), name='order'),
    path('make-order/', MakeOrderView.as_view(), name='make_order')
]


