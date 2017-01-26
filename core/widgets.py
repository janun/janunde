from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_text


class DateInput(forms.DateInput):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<span class="dateinput"><input{} /><a href="#" class="dateinput__open hide@no-js"><i class="icon-calendar"></i></a><span class="extra-help">Datum</span></span>', flatatt(final_attrs))


class TimeInput(forms.DateInput):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self.format_value(value))
        return format_html('<span class="timeinput"><input{} /><a href="#" class="timeinput__open hide@no-js"><i class="icon-clock"></i></a><span class="extra-help">Uhrzeit</span></span>', flatatt(final_attrs))


class SplitDateTimeWidget(forms.MultiWidget):
    """
    A Widget that splits datetime input into two <input type="text"> boxes.
    """
    supports_microseconds = False

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (
            DateInput(attrs=attrs, format=date_format),
            TimeInput(attrs=attrs, format=time_format),
        )
        super(SplitDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value = to_current_timezone(value)
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]
