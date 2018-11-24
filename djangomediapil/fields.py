import os
import json
import datetime as dt
from django import forms
from django.db import models
from django.core import exceptions
from django.utils.translation import ugettext_lazy as _

from .mediaPIL import MediaPIL
from .widgets import ImagePILWidget


class ImagePILField(models.TextField):
    description = "Image PIL Field"

    def __init__(self, pathway="", point=(50, 50), quality=90,
                 upload_to=".", *args, **kwargs):

        self.blank = kwargs.get('blank', False)

        if pathway is None:
            pathway = ""

        self.default_kwargs = {
            'pathway': pathway,
            'point': point,
            'quality': quality,
            'upload_to': upload_to,
        }
        kwargs['default'] = json.dumps(
            self.default_kwargs, ensure_ascii=False)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        try:
            if value is None:
                return self.default_kwargs
            if type(value) == str and '{' not in value:
                kw = self.default_kwargs.copy()
                kw['pathway'] = value
                return kw
            return json.loads(value)
        except Exception as e:
            return self.default_kwargs

    def clean(self, value, model_instance):
        val = json.loads(value)
        if not val.get('pathway') and not self.blank:
            raise forms.ValidationError(
                _('This field is required'), code='invalid')
        return value

    def get_prep_value(self, value):
        if type(value) == str:
            return value
        return json.dumps(value, ensure_ascii=False)

    def value_to_string(self, obj):
        return self.get_prep_value(obj.image)

    def to_python(self, value):
        return self.from_db_value(value=value)

    def formfield(self, **kwargs):
        widget = kwargs.get('widget')
        if 'AdminTextareaWidget' in str(widget):
            kwargs['widget'] = ImagePILWidget
        return super().formfield(**kwargs)
