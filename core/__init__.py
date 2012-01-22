#-*- coding=utf-8

from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.core import management
from django.db import models

from south.exceptions import NoMigrations
from south.migration.base import Migrations

import yaml

FIELD_NAMES_MAP = {'int': models.IntegerField,
                   'float': models.FloatField,
                   'char': models.CharField,
                   'text': models.TextField,
                   'date': models.DateField,
                   'datetime': models.DateTimeField}

FIELDS_REQUIRED_DEFAULTS = {'max_length': 100}

APP_LABEL = 'core'

class ModelsCreator():
    def __init__(self, stream):
        self.models_settings = yaml.load(stream)

    def create_models(self):
        for model_name, model_info in self.models_settings.iteritems():
            class Meta:
                pass

            setattr(Meta, 'app_label', APP_LABEL)
            setattr(Meta, 'verbose_name', model_info['title'])
            setattr(Meta, 'verbose_name_plural', model_info['title'])
            
            fields = self._create_model_fields(model_info['fields'])
            fields['Meta'] = Meta
            fields['__module__'] = APP_LABEL + '.models'

            cls = type(model_name, (models.Model, ), fields)

            try:
                admin.site.register(cls)
            except AlreadyRegistered:
                admin.site.unregister(cls)
                admin.site.register(cls)

        try:
            try:
                try:
                    Migrations(APP_LABEL)
                    management.call_command('schemamigration', 'core', auto=True, verbosity=0)
                except NoMigrations:
                    management.call_command('schemamigration', 'core', initial=True, verbosity=0)
            except (SystemExit, Exception):
                pass
            Migrations._clear_cache()
            try:
                management.call_command('migrate', 'core')
            except SystemExit:
                pass
        except Exception as e:
            pass

    def _create_model_fields(self, yaml_dict):
        fields = {}
        for params in yaml_dict:
            field_name = params['id']
            field_verbose_name = params['title']
            field_type = FIELD_NAMES_MAP[params['type'].lower()]
            fields[field_name] = field_type(verbose_name=field_verbose_name, max_length=100)
        return fields
