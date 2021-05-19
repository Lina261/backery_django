from django.shortcuts import render
from django.views.generic import DetailView, View
from django.contrib.contenttypes.models import ContentType
from .models import Bread, Pie, Cake, Sweets, Category, LatestProducts, Customer, Cart, CartProduct
from .mixins import CategoryDetailMixin, CartMixin
from django.http import HttpResponseRedirect
from .forms import OrderForm
from django.contrib import messages
from .utils import calc_cart
from django.db import transaction

# def test_view(request):
#     categories = Category.objects.get_categories_for_left_sidebar()
    
#     return render(request, 'base.html', {'categories': categories})

class BaseView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('bread', 'pie', 'sweets', 'cake')
        context = {
            'categories': categories,
            'products' : products,
            'cart': self.cart
        }
        
        return render(request, 'base.html', context)



class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS= {
        'bread': Bread,
        'pie': Pie,
        'cake': Cake,
        'sweets' : Sweets
    }

    def dispatch(self, request, *args, **kwargs):
        
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)
            
        
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context
    



class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context
    



class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug = product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user = self.cart.owner, cart=self.cart, content_type = content_type, object_id=product.id
        )
        if created:
             self.cart.product.add(cart_product)
        calc_cart(self.cart)
        return HttpResponseRedirect('/cart/')



class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug = product_slug)
        cart_product= CartProduct.objects.get(
            user = self.cart.owner, cart=self.cart, content_type = content_type, object_id=product.id
        )
        self.cart.product.remove(cart_product)
        cart_product.delete()
        calc_cart(self.cart)
        return HttpResponseRedirect('/cart/')


class ChangeCountView(CartMixin, View):
    def post(self,request, *args, **kwargs ):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug = product_slug)
        cart_product= CartProduct.objects.get(
            user = self.cart.owner, cart=self.cart, content_type = content_type, object_id=product.id
        )
        count = int(request.POST.get('count'))
        print(count)
        cart_product.count = count
        cart_product.save()
        calc_cart(self.cart)
        return HttpResponseRedirect('/cart/')

class CartView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart' : self.cart,
            'categories' : categories
        }
        return render(request, 'cart.html', context)


class OrderView(CartMixin, View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart' : self.cart,
            'categories' : categories,
            'form' : form
        }
        return render(request, 'order.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, "Спасибо за заказ!!")
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/order/')