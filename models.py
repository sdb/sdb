from django import forms
from django.core import exceptions
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils import simplejson
from django.utils.translation import ugettext_lazy as _

from django.forms.widgets import Textarea
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.html import conditional_escape


class DictionaryField(models.Field):
    description = _("Dictionary object")
    
    __metaclass__ = models.SubfieldBase

    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        if value is None:
            return None
        elif value == "":
            return None
        elif isinstance(value, basestring):
            try:
                return simplejson.loads(value)
            except (ValueError, TypeError):
                raise exceptions.ValidationError(self.error_messages['invalid'])
        
        if isinstance(value, dict):
            return value
        else:
            return {}
        
    def get_prep_value(self, value):
        if not value:
            return ""
        elif isinstance(value, basestring):
            return value
        else:
            return simplejson.dumps(value)
            
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)
    
    def clean(self, value, model_instance):
        value = super(DictionaryField, self).clean(value, model_instance)
        return self.get_prep_value(value)
    
    def formfield(self, **kwargs):
        defaults = {'widget': DictionaryWidget}
        defaults.update(kwargs)
        return super(DictionaryField, self).formfield(**defaults)


class DictionaryWidget(Textarea):
    def __init__(self, attrs=None):
        # The 'rows' and 'cols' attributes are required for HTML correctness.
        super(DictionaryWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(simplejson.dumps(value) if value != None and value != '' else '')))

