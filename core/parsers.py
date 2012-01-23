#-*- coding=utf-8
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.core import management
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models.loading import cache as models_cache

from south.exceptions import NoMigrations
from south.migration.base import Migrations

import yaml

FIELD_NAMES_MAP = {'char':'char', 'str':'char', 'string':'char',
                   'int':'int', 'integer':'int', 'long': 'long',
                   'float': 'float', 'double': 'float',
                   'date': 'date',
                   'datetime': 'datetime',
                   'text': 'text',
                   'time': 'time'}

FIELD_TYPES_MAP = {'int': models.IntegerField,
                   'float': models.FloatField,
                   'char': models.CharField,
                   'text': models.TextField,
                   'date': models.DateField,
                   'datetime': models.DateTimeField,
                   'time': models.TimeField}

FIELDS_REQUIRED_DEFAULTS = {'char': {'max_length': 100 }}

class ModelsCreator():
    def __init__(self, stream):
        self.models_settings = yaml.load(stream)

    def create_models(self):
        models_cache.app_models[settings.DYNAMIC_MODELS_APP] = SortedDict()
        for model_name, model_info in self.models_settings.iteritems():
            m_name = "".join([s.capitalize() for s in str(model_name).split('_')])
            class Meta:
                pass

            setattr(Meta, 'app_label', settings.DYNAMIC_MODELS_APP)
            setattr(Meta, 'verbose_name', model_info['title'])
            setattr(Meta, 'verbose_name_plural', model_info['title'])
            
            fields = self._create_model_fields(model_info['fields'])
            fields['Meta'] = Meta
            fields['__module__'] = settings.DYNAMIC_MODELS_APP + '.models'

            cls = type(m_name, (models.Model, ), fields)

            try:
                admin.site.register(cls)
            except AlreadyRegistered:
                pass

        try:
            try:
                try:
                    Migrations(settings.DYNAMIC_MODELS_APP)
                    management.call_command('schemamigration', settings.DYNAMIC_MODELS_APP, auto=True)
                except NoMigrations:
                    management.call_command('schemamigration', settings.DYNAMIC_MODELS_APP, initial=True)
            except (SystemExit, Exception):
                pass
            Migrations._clear_cache()
            try:
                management.call_command('migrate', settings.DYNAMIC_MODELS_APP)
            except SystemExit:
                pass
        except Exception:
            pass

    def _create_model_fields(self, yaml_dict):
        """
        Parse yaml description of model fields
        """
        fields = {}
        for params in yaml_dict:
            field_name = params.pop('id', None)
            if not field_name:
                raise ImproperlyConfigured(_(u"Field id must be provided"))

            # inner field type name
            field_type_name = FIELD_NAMES_MAP.get(params.pop('type', '').lower())
            if not field_type_name:
                raise ImproperlyConfigured(_(u"Unknown field type '%s'" % params['type'].lower()))

            field_verbose_name = params.pop('title', field_name)

            field_type = FIELD_TYPES_MAP[field_type_name]

            # specific defaults for type
            opts = FIELDS_REQUIRED_DEFAULTS.get(field_type_name, {})
            # null and blank default for all kind of fields
            opts['null'] = True
            opts['blank'] = True
            # remainded options in settings file
            opts.update(params)

            fields[field_name] = field_type(verbose_name=field_verbose_name, **opts)
        return fields