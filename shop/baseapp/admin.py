# библиотека для проверки размера фото
from PIL import Image

# django
from django.contrib import admin
from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.utils.safestring import mark_safe   # превращает строку в html код со стилями и тэгом

# Мои
from .models import *


class SmartphoneAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if not instance.sd:
            self.fields['sd_volum_max'].widget.attrs.update({
                'readonly': True, 
                'style': 'background: lightgray;'
            })

    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_volum_max'] = None
        return self.cleaned_data


#? пример как можно использовать PIL, чтобы он обрезал фото
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     image = models.ImageField(default='default.jpg', upload_to=upload_profile)

#     def __str__(self):
#         return f'Profile {self.user.username}'

#     def save(self):
#         super().save()
#         img = Image.open(self.image.path)

#         if img.height > 300 or img.width > 300:
#             output_size = (300, 300)
#             img.thumbnail(output_size)
#             img.save(self.image.path)

# Проверка на размер загружаемой фотографии в админке
class NotebookAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            '''<span style="color:red; font-size:14px;">При загрузке изображения с разрешением больше {}x{} оно будет обрезано!</span>
            '''.format(
                *Product.MAX_RESOLUTION
            )
        )

    # def clean_image(self):
    #     image = self.cleaned_data['image']      # это сам файл
    #     img = Image.open(image)         # это кортеж со значениями файлы, размеры и т.п.
    #     min_width, min_height = Product.MIN_RESOLUTION     # обязательно сначала 
    #     max_width, max_height = Product.MAX_RESOLUTION     # надо указывать ширину!

    #     if image.size > Product.MAX_IMAGE_SIZE:
    #         raise ValidationError('Размер изображения не должен превышать 3 мегабайта!')
    #     if img.width < min_width or img.height < min_height:
    #         raise ValidationError('Разрешение изображения меньше минимального!')
    #     if img.width > max_width or img.height > max_height:
    #         raise ValidationError('Разрешение изображения больше максимального!')
    #     return image


# админка ноутбука
class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# админка смартфона
class SmartphoneAdmin(admin.ModelAdmin):

    change_form_template = 'admin.html'
    form = SmartphoneAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
