import re
from urllib.request import urlopen
from django.core.exceptions import ValidationError
from django.db import models
from django import forms

from django.template.loader import render_to_string
from django.forms.fields import EMPTY_VALUES
from django.utils.translation import ugettext as _



class PrettyURLField(models.URLField):
    """
     * accepts url without scheme
     * adds default scheme of http:// if no scheme given
     * tries to retrieve url to validate
     * doesnt retrieve url if not changed
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__orig_value = ""

    def has_scheme(self, value):
        return bool(re.match(r'^\w+:', value))

    def can_open_url(self, value):
        try:
            response = urlopen(value)
            return True
        except IOError:
            return False

    def has_changed(self, value):
        ret = self.__orig_value != value
        self.__orig_value = value
        return ret

    def to_python(self, value):
        if value and isinstance(value, str):
            if not self.has_scheme(value):
                return "http://" + value
            # if self.has_changed(value) and not self.can_open_url(value):
            #     raise ValidationError("Kann diese Website nicht aufrufen.")
        return super().to_python(value)

    def formfield(self, **kwargs):
        from django import forms
        defaults = {
            'form_class': forms.CharField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class FacebookEventURLField(PrettyURLField):
    """validates that its a valid facebook event url and removes extraneous stuff"""
    facebook_event_regex = r'(^http(?:s)?://(?:www\.)?facebook\.com/events/\d+)'

    def to_python(self, value):
        value = super().to_python(value)
        if value and isinstance(value, str):
            match = re.match(self.facebook_event_regex, value)
            if match:
                return match.groups()[0]
            else:
                raise ValidationError("Das ist keine gültige Facebook-Event-URL")
        return value


class FacebookProfileURLField(PrettyURLField):
    """validates that its a valid facebook profile url and removes extraneous stuff"""
    facebook_profile_regex = r'(?:https?:\/\/)?(?:www\.)?facebook\.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[\w\-]*\/)*([\w\-\.]*)'

    def to_python(self, value):
        value = super().to_python(value)
        if value and isinstance(value, str):
            match = re.match(self.facebook_profile_regex, value)
            if match:
                return match.string
            else:
                raise ValidationError("Das ist keine gültige Facebook-Profil-URL")
        return value




# class RangeWidget(forms.MultiWidget):
#     def __init__(self, widget, *args, **kwargs):
#         widgets = (widget, widget)
#         super(RangeWidget, self).__init__(widgets=widgets, *args, **kwargs)
#
#     def decompress(self, value):
#         return value
#
#     def format_output(self, rendered_widgets):
#         widget_context = {'min': rendered_widgets[0], 'max': rendered_widgets[1],}
#         return render_to_string('widgets/range_widget.html', widget_context)
#
# class RangeField(forms.MultiValueField):
#     default_error_messages = {
#         'invalid_start': _(u'Enter a valid start value.'),
#         'invalid_end': _(u'Enter a valid end value.'),
#     }
#
#     def __init__(self, field_class, widget=forms.TextInput, *args, **kwargs):
#         if not 'initial' in kwargs:
#             kwargs['initial'] = ['','']
#
#         fields = (field_class(), field_class())
#
#         super(RangeField, self).__init__(
#                 fields=fields,
#                 widget=RangeWidget(widget),
#                 *args, **kwargs
#                 )
#
#     def compress(self, data_list):
#         if data_list:
#             return [self.fields[0].clean(data_list[0]),self.fields[1].clean(data_list[1])]
#
#         return None
