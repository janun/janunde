import re
from urllib.request import urlopen
from django.core.exceptions import ValidationError
from django.db import models

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
            if self.has_changed(value) and not self.can_open_url(value):
                raise ValidationError("Kann diese Website nicht aufrufen.")
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
