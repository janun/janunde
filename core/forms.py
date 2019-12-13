from django import forms
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.core.models import Page


class ShortTitleForm(WagtailAdminPageForm):
    """can be used as base_form_class to limit the length of the title field
    unfortunately title_max_length cannot be changed in subclasses
    """
    title_max_length = 50
    title = forms.CharField(
        label="Titel",
        max_length=title_max_length,
        help_text="%i Zeichen sind erlaubt." % title_max_length
    )
