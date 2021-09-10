from django import template
from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import DetailView, View

from .models import Notebook, Smartphone, Category
from .mixins import CategoryDetailMixin


class BaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        return render(request, 'base.html', {'categories': categories})


# def test_view(request):
#     categories = Category.objects.get_categories_for_left_sidebar()
#     return render(request, 'base.html', {'categories': categories})


class ProductDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': Smartphone
    }
    

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    # model = Model
    # queryset = Model.objects.all()
    context_object_name = 'product' # product - передается в шаблоны, таким образом мы можем работать с шаблоном через product и вызывать все атрибуты, которые есть в модели, так как сама вьюшка ProductDetailView связана с соответствующей моделью (Notebook/Smartphone)
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'
    

class CategoryDetailView(CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'