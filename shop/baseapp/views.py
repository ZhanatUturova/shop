from django.db.models.base import Model
from django.shortcuts import render
from django.views.generic import DetailView

from .models import Notebook, Smartphone

# Create your views here.
def test_view(request):
    return render(request, 'base.html', {})


class ProductDetailView(DetailView):

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
    