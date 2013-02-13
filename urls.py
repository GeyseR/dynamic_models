import io
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from core.parsers import ModelsCreator

admin.autodiscover()

stream = io.open(settings.DYNAMIC_MODELS_FILE, encoding='utf-8')
creator = ModelsCreator(stream)
creator.create_models()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', 'core.views.index', name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^load_schema/$', 'core.views.load_scheme', name='load_scheme'),
    url(r'^(?P<model_name>\w+)/$', 'core.views.model_items', name='get_model_items'),
)
