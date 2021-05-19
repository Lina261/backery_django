from django.contrib import admin
from .models import *
from django.forms import ModelChoiceField, ModelForm, ValidationError
from PIL import Image
from django.utils.safestring import mark_safe



# class BreadAdminForm(ModelForm):

#     VALID_RESOLUTION = (400,400)
#     MAX_RESOLUTION = (1000, 1000)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['image'].help_text=mark_safe('<span style="color:red; font-size:14px;">Загружайте изображения с расширением не более  {}x{} !</span>'.format(*Product.MAX_RESOLUTION))

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'category':
    #         return ModelChoiceField(Category.objects.filter(slug='breads'))
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
class BreadAdminForm(ModelForm):

    VALID_RESOLUTION = (400,400)
    MAX_RESOLUTION = (1000, 1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text=mark_safe('<span style="color:red; font-size:14px;">Загружайте изображения с расширением не более  {}x{} !</span>'.format(*Product.MAX_RESOLUTION))


    def clean_image(self):
    
        image = self.cleaned_data['image']
        img = Image.open(image)
        print(img.width, img.height)
        max_height, max_width = Product.MAX_RESOLUTION
        min_height, min_width = Product.VALID_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError("Размер изображения не должне превышать 3МБ!")
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Разрешение изображения больше максимального!')
        return image

class PieAdminForm(ModelForm):
    
    VALID_RESOLUTION = (400,400)
    MAX_RESOLUTION = (1000, 1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text=mark_safe('<span style="color:red; font-size:14px;">Загружайте изображения с расширением не более  {}x{} !</span>'.format(*Product.MAX_RESOLUTION))


    def clean_image(self):
    
        image = self.cleaned_data['image']
        img = Image.open(image)
        print(img.width, img.height)
        max_height, max_width = Product.MAX_RESOLUTION
        min_height, min_width = Product.VALID_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError("Размер изображения не должне превышать 3МБ!")
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Разрешение изображения больше максимального!')
        return image


class CakeAdminForm(ModelForm):
    
    VALID_RESOLUTION = (400,400)
    MAX_RESOLUTION = (1000, 1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text=mark_safe('<span style="color:red; font-size:14px;">Загружайте изображения с расширением не более  {}x{} !</span>'.format(*Product.MAX_RESOLUTION))


    def clean_image(self):
    
        image = self.cleaned_data['image']
        img = Image.open(image)
        print(img.width, img.height)
        max_height, max_width = Product.MAX_RESOLUTION
        min_height, min_width = Product.VALID_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError("Размер изображения не должне превышать 3МБ!")
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Разрешение изображения больше максимального!')
        return image


class SweetsAdminForm(ModelForm):
    
    VALID_RESOLUTION = (400,400)
    MAX_RESOLUTION = (1000, 1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text=mark_safe('<span style="color:red; font-size:14px;">Загружайте изображения с расширением не более  {}x{} !</span>'.format(*Product.MAX_RESOLUTION))


    def clean_image(self):
    
        image = self.cleaned_data['image']
        img = Image.open(image)
        print(img.width, img.height)
        max_height, max_width = Product.MAX_RESOLUTION
        min_height, min_width = Product.VALID_RESOLUTION
        if image.size > Product.MAX_IMAGE_SIZE:
            raise ValidationError("Размер изображения не должне превышать 3МБ!")
        if img.height < min_height or img.width < min_width:
            raise ValidationError('Разрешение изображения меньше минимального!')
        if img.height > max_height or img.width > max_width:
            raise ValidationError('Разрешение изображения больше максимального!')
        return image






class BreadAdmin(admin.ModelAdmin):
    form = BreadAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='breads'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    #  def get_fields(self, request, obj):
    #         fields = super(BreadAdmin, self).get_fields(request, obj)
    #         fields.remove(fields[0])
    #         return fields
        

class PieAdmin(admin.ModelAdmin):
    form = PieAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='pie'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CakeAdmin(admin.ModelAdmin):
    form = CakeAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='cake'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)




class SweetsAdmin(admin.ModelAdmin):
    form = SweetsAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='sweets'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Category)
admin.site.register(Bread, BreadAdmin)
admin.site.register(Pie, PieAdmin)
admin.site.register(Cake, CakeAdmin)
admin.site.register(Sweets, SweetsAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)

