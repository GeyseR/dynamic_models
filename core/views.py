#-*- coding=utf-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.loading import get_models, load_app, get_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils import simplejson
from django.views.decorators.csrf import csrf_protect
from core.forms import FileForm
from core.parsers import ModelsCreator

def get_dynamic_models():
    app = load_app(settings.DYNAMIC_MODELS_APP)
    models = [(model._meta.object_name, model._meta.verbose_name) for model in get_models(app)]
    return models


def index(request):
    """
    Render list of all dynamic models in app
    """
    return render(request, 'index.html',
            {'app': settings.DYNAMIC_MODELS_APP,
             'models': get_dynamic_models(),
             'form': FileForm()})


def model_items(request, model_name):
    """
    Render list of items for <model_name> model
    When request is ajax returns json data with field verbose names and items
    """

    model = get_model(settings.DYNAMIC_MODELS_APP, model_name)
    fields = sorted(
        [(field, field.name, field.verbose_name) for field in model._meta.fields],
        cmp=lambda x, y: cmp(x[2], y[2]))

    items = []
    for instance in model.objects.all():
        item_fields = []
        for f in fields:
            item_fields.append(unicode(f[0].value_from_object(instance)))
        items.append(item_fields)

    if not request.is_ajax():
        return render(request, 'index.html',
                {'app': settings.DYNAMIC_MODELS_APP,
                 'models': get_dynamic_models(),
                 'model_name': model_name,
                 'fields': fields,
                 'items': items,
                 'form': FileForm()
            }
        )
    else:
        data = {'items': items, 'field_verbose_names': [f[2] for f in fields]}
        return HttpResponse(simplejson.dumps(data, ensure_ascii=False), mimetype="application/json")


@csrf_protect
def load_scheme(request):
    """
    Reload schema from yaml file on POST request
    """
    if request.method == 'GET':
        # maybe we have model with 'load_scheme' name
        return model_items(request, 'load_scheme')

    form = FileForm(request.POST, request.FILES)
    if form.is_valid():
        creator = ModelsCreator(form.cleaned_data['upload_file'].file)
        creator.create_models()
    return HttpResponseRedirect(reverse('index'))