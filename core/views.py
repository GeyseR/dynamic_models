#-*- coding=utf-8
from django.conf import settings
from django.db.models.loading import get_models, load_app, get_model
from django.shortcuts import render

def get_dynamic_models():
    app = load_app(settings.DYNAMIC_MODELS_APP)
    models = [(model._meta.object_name, model._meta.verbose_name) for model in get_models(app)]
    return models


def index(request):
    return render(request, 'index.html', {'models': get_dynamic_models()})


def model_items(request, model_name):
    fields = [field.name for field in get_model(settings.DYNAMIC_MODELS_APP, model_name)._meta.fields]
    return render(request, 'index.html',
            {'models': get_dynamic_models(),
             'model_name': model_name,
             'fields': fields
        }
    )