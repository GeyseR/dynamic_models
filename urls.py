import io
from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
from django.core import management
from core import ModelsCreator

admin.autodiscover()

stream = io.open(settings.DYNAMIC_MODELS_FILE, encoding='utf-8')
creator = ModelsCreator(stream)
creator.create_models()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dynamic_models.views.home', name='home'),
    # url(r'^dynamic_models/', include('dynamic_models.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', 'core.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<model_name>\w+)/$', 'core.views.model_items', name='get_model_items'),
)
