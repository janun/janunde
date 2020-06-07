from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


class SubMenuInternalPageValue(blocks.StructValue):
    def get_title(self):
        return self.get("title") or self.get("page").title

    def get_subtitle(self):
        try:
            return self.get("subtitle") or self.get("page").specific.subtitle
        except AttributeError:
            return ""


class InternalPageBlock(blocks.StructBlock):
    """Link to internal page (top level item)"""

    page = blocks.PageChooserBlock(label="Seite")
    title = blocks.CharBlock(
        label="Titel", help_text="Überschreibt Titel der Seite", required=False,
    )

    class Meta:
        label = "Interne Seite"
        icon = "link"
        value_class = SubMenuInternalPageValue


class SubMenuInternalPageBlock(blocks.StructBlock):
    """Link to internal page in submenu"""

    page = blocks.PageChooserBlock(label="Seite")
    title = blocks.CharBlock(
        label="Titel", required=False, help_text="Überschreibt Titel der Seite",
    )
    subtitle = blocks.CharBlock(
        label="Untertitel",
        required=False,
        help_text="Überschreibt Untertitel der Seite",
    )

    class Meta:
        label = "Interne Seite"
        icon = "link"
        value_class = SubMenuInternalPageValue


class SubMenuCategoryBlock(blocks.StructBlock):
    """Category in submenu"""

    title = blocks.CharBlock(label="Titel")
    submenu = blocks.StreamBlock(
        [("internal_page", SubMenuInternalPageBlock())], label="Untermenü"
    )

    class Meta:
        label = "Kategorie"
        icon = "folder"


class SubMenuBlock(blocks.StructBlock):
    """Submenu (toplevel item)"""

    title = blocks.CharBlock(label="Titel")
    submenu = blocks.StreamBlock(
        [("category", SubMenuCategoryBlock())], label="Menü-Einträge"
    )

    class Meta:
        label = "Untermenü"
        icon = "folder"


@register_setting
class NavbarSettings(BaseSetting):
    """Settings for the navbar"""

    menu = StreamField(
        [("submenu", SubMenuBlock()), ("internal_page", InternalPageBlock())]
    )

    panels = [
        StreamFieldPanel("menu"),
    ]

    class Meta:
        verbose_name = "Menü"
