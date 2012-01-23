from django import forms
from django.utils.translation import ugettext as _

class FileForm(forms.Form):
    upload_file = forms.FileField(label=_(u"Yaml file with scheme description"))