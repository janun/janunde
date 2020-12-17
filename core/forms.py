from django import forms
from wagtail.admin import widgets
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.forms.collections import BaseCollectionMemberForm

from wagtailmedia.permissions import permission_policy as media_permission_policy


class ShortTitleForm(WagtailAdminPageForm):
    """can be used as base_form_class to limit the length of the title field
    unfortunately title_max_length cannot be changed in subclasses
    """

    title_max_length = 50
    title = forms.CharField(
        label="Titel",
        max_length=title_max_length,
        help_text="%i Zeichen sind erlaubt." % title_max_length,
    )


class BaseMediaForm(BaseCollectionMemberForm):
    class Meta:
        widgets = {
            "tags": widgets.AdminTagWidget,
            "file": forms.FileInput,
            "thumbnail": forms.ClearableFileInput,
        }

    permission_policy = media_permission_policy

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name in ("width", "height", "duration"):
            if name in self.fields:
                del self.fields[name]

        if self.instance.type == "audio":
            for name in ("thumbnail",):
                if name in self.fields:
                    del self.fields[name]
