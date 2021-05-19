from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType #это мини фреймворк который видит все модели в пр-ме
from django.contrib.contenttypes.fields import GenericForeignKey
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from django.urls import reverse
from django.forms import  ValidationError
from django.utils import timezone


User = get_user_model()  

def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, view_name):
    ct_model = obj.__class__._meta.model_name
    return reverse(view_name, kwargs={'ct_model': ct_model, 'slug':obj.slug})



class MinResolutionErrorException(Exception):
    pass


class MaxResolutionErrorException(Exception):
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products =[]
        ct_models = ContentType.objects.filter(model__in = args)
        for ct_model in ct_models:# вызыввем у контент тайп модели ее родительский класс,них можель класс обращаясь к модели
                model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
                products.extend(model_products)# собираем продукты для главной страницы
        if with_respect_to:
            ct_model =ContentType.objects.filter(model = with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True)
        return products
    
class LatestProducts:
    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Хлеб' : 'bread__count',
        'Торты и пироги' : 'pie__count',
        'Пирожные' : 'cake__count',
        'Конфеты' : 'sweets__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('bread', 'pie', 'cake', 'sweets')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name = c.name, url = c.get_absolute_url(), count= getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs 
        ]
        return data


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    


class Product(models.Model):# каркас для самого продукта


    VALID_RESOLUTION = (400,400)
    MAX_RESOLUTION = (1000, 1000)
    MAX_IMAGE_SIZE = 3145728

    class Meta: # если модель абстрактная для нее нельзя создать миграцию
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Стоимость')

    def __str__(self):
        return self.title


    def get_model_name(self):
        return self.__class__.__name__.lower()

    def save(self,*args, **kwargs):
        image = self.image
        img = Image.open(image)
        max_height, max_width = self.MAX_RESOLUTION
        min_height, min_width = self.VALID_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException('Разрешение изображения меньше минимального!')
        if img.height > max_height or img.width > max_width:
            raise MaxResolutionErrorException('Разрешение изображения больше максимального!')
        # image = self.image
        # img = Image.open(image)
        # new_img = img.convert('RGB')
        # resized_new_img = new_img.resize((200,200), Image.ANTIALIAS)
        # filestream = BytesIO()
        # resized_new_img.save(filestream,'JPEG', quality=90 )
        # filestream.seek(0)
        # name = '{}.{}'.format(*self.image.name.split('.'))
        # print(self.image.name, name)
        # self.image = InMemoryUploadedFile(filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None )
        super().save(*args, **kwargs)


        



class Bread(Product):
    composition = models.TextField(max_length=255, verbose_name='Состав')
    weight = models.CharField(max_length=20, verbose_name='Вес')
    expiration_date = models.CharField(max_length=20, verbose_name='Срок годности')
    flour=models.CharField(max_length=20, verbose_name='На основе муки')

    def get_absolute_url(self):
       
        return get_product_url(self, 'product_detail')

   
    
    # def __str__(self):
    #     return "{} : {}".format(self.category.name, self.title)

    

    
    
   

    
class Cake(Product):
    # сategory = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE, default='Торты')
    composition = models.TextField(max_length=255, verbose_name='Состав')
    weight = models.CharField(max_length=20, verbose_name='Вес')
    expiration_date = models.CharField(max_length=20, verbose_name='Срок годности')
    cream=models.CharField(max_length=20, verbose_name='Крем')
    dough=models.CharField(max_length=20, verbose_name='Тесто')

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

   

class Pie(Product):
    # сategory = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE, default='Пироги')
    composition = models.TextField(max_length=255, verbose_name='Состав')
    weight = models.CharField(max_length=20, verbose_name='Вес')
    expiration_date = models.CharField(max_length=20, verbose_name='Срок годности')
    stuffing =models.TextField(max_length=20, verbose_name='Начинка')

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    


class Sweets(Product):
    # сategory = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.CASCADE, default='Конфеты')
    quantity = models.CharField(max_length=20, verbose_name='Количество в упаковке')
    weight = models.CharField(max_length=20, verbose_name='Вес')
    tastes = models.TextField(max_length=255, verbose_name='Вкусы')

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

   



class CartProduct(models.Model):
    user = models.ForeignKey(
        'Customer', verbose_name='Заказчик', on_delete=models.CASCADE)
    cart = models.ForeignKey(
        'Cart', verbose_name='Корзина', on_delete=models.CASCADE,related_name='related_product')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE) #то есть покажет все модели которые есть в проекте
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    count = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Сумма')

    def __str__(self):
        return "Продукт:{} (для корзины)".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.total_price = self.count * self.content_object.price
        super().save(*args, **kwargs)

    def get_model_name(self):
        return self.__class__._meta.model_name



class Cart(models.Model):
    owner = models.ForeignKey(
        'Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    product = models.ManyToManyField(CartProduct, blank=True, related_name='related_card')
    total_products = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(
        max_digits=9, default=0, decimal_places=2, verbose_name='Сумма')
    in_order = models.BooleanField(default=False) 
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    # def save(self, *args, **kwargs):
    #     cart_data = self.product.aggregate(models.Sum('total_price'), models.Count('id'))
    #     print(cart_data )
    #     if cart_data.get('total_price__sum'):
    #         self.total_price = cart_data['total_price__sum']
    #     else: 
    #         self.total_price=0
    #     self.total_products = cart_data['id__count']
    #     super().save(*args, **kwargs)

class Customer(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer')

    def __str__(self):
        return 'Покупатель:{} {}'.format(self.user.first_name, self.user.last_name)



class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUSES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer =models.ForeignKey(Customer, verbose_name='Покупатель', on_delete = models.CASCADE, related_name='related_orders')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices=STATUSES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Доставка',
        choices=BUYING_TYPES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)

    def __str__(self):
        return str(self.id)

