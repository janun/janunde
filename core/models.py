from __future__ import unicode_literals
import datetime
from datetime import timedelta
from unidecode import unidecode
import html2text
from bs4 import BeautifulSoup
from softhyphen.html import hyphenate

from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils import timezone
from django.utils.text import slugify
from django.utils.six import text_type
from django.utils.text import Truncator
from django.template.loader import render_to_string

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    StreamFieldPanel,
    FieldRowPanel,
    MultiFieldPanel,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, PageManager, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.admin.utils import send_mail  # pylint: disable=no-name-in-module
from wagtail.contrib.forms.forms import WagtailAdminPageForm
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSetting, register_setting

from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from core.fields import FacebookProfileURLField, PrettyURLField
from .blocks import StandardStreamBlock, HomePageStreamBlock
from .images import AttributedImage as Image
from .forms import ShortTitleForm


COLOR_CHOICES = [
    ("green", "Grün"),
    ("red", "Rot"),
    ("blue", "Blau"),
    ("orange", "Orange"),
]

TEXT_DIRECTION_CHOICES = [
    ("ltr", "Links nach Rechts"),
    ("rtl", "Rechts nach Links"),
]


def stream2text(stream, truncate=False):
    h = html2text.HTML2Text()
    h.ignore_links = True
    for block in stream:
        if block.block_type == "paragraph":
            text = h.handle(block.value.source)
            if truncate:
                return Truncator(text).words(truncate)
            else:
                return text


def stream2image(stream):
    for block in stream:
        if block.block_type == "image":
            return block.value["image"]
        if block.block_type == "several_images":
            return block.value[0]["image"]


class HyphenatedTitleMixin(models.Model):
    """provides hyphenated_title with shy tags"""

    hyphenated_title = models.CharField(max_length=255, null=True, blank=True,)

    def save(self, *args, **kwargs):
        self.hyphenated_title = hyphenate(self.title, language="de-de")
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class BasePage(Page, HyphenatedTitleMixin):
    """basic functionality for all our pages"""

    og_type = "article"
    partial_template_name = "core/_partial.html"
    is_creatable = False

    def get_description(self):
        """Short description text for SEO"""
        for attr in ("search_description", "subtitle", "role"):
            if hasattr(self, attr) and getattr(self, attr):
                return getattr(self, attr)
        for attr in ("body", "content", "text"):
            if hasattr(self, attr) and getattr(self, attr):
                return stream2text(getattr(self, attr), 25)
        if hasattr(type(self)._meta, "verbose_name"):
            return type(self)._meta.verbose_name
        return ""

    def get_image(self):
        """image for SEO"""
        for attr in ("main_image", "feed_image", "logo", "photo", "header_image"):
            if hasattr(self, attr) and getattr(self, attr):
                return getattr(self, attr)
        for attr in ("body", "content", "text"):
            if hasattr(self, attr) and getattr(self, attr):
                return stream2image(getattr(self, attr))
        return None

    def serve_preview(self, request, mode_name):
        request.preview_timestamp = datetime.datetime.now()
        return super(BasePage, self).serve_preview(request, mode_name)


def get_in_14_days():
    return timezone.now() + timedelta(days=14)


class PublishedAtFromGoLiveAtMixin(object):
    """
    set the first_published_at date to the go_live_at
    attribute on live pages on save.
    Thus enabling editors to create pages in the past
    """

    def clean(self):
        super().clean()
        if self.live and self.go_live_at:
            self.first_published_at = self.go_live_at

    class Meta:
        abstract = True


class FallbackImageMixin(object):
    """
    of main_image_field is not set, set it to a random image,
    that's tagged with fallback_image_tag
    """

    main_image_field = "main_image"
    fallback_image_tag = ""

    def clean(self):
        super().clean()
        if not self.fallback_image_tag:
            self.fallback_image_tag = type(self).__name__.lower() + "-fallback"
        if not self.__getattribute__(self.main_image_field):
            self.__setattr__(
                self.main_image_field,
                Image.objects.filter(tags__name=self.fallback_image_tag)
                .order_by("?")
                .first(),
            )

    class Meta:
        abstract = True


class HeaderMixin(models.Model):
    """
    A Page with big heading bar,
    containing a heading and a header_image
    typically for top-level pages

    templates of subclasses should include core/_pageheader.html
    """

    heading = models.CharField("Überschrift", max_length=255, blank=True,)
    header_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Header-Bild",
    )
    panels = [
        FieldPanel("heading", classname="title"),
        ImageChooserPanel("header_image"),
    ]

    class Meta:
        abstract = True


class StandardPage(BasePage):
    """
    simple "just a page"
    """

    title_color = models.CharField(
        "Titelfarbe",
        choices=COLOR_CHOICES,
        max_length=255,
        default="green",
        help_text="Der Titel wird in dieser Farbe angezeigt.",
    )

    text_direction = models.CharField(
        "Textrichtung",
        choices=TEXT_DIRECTION_CHOICES,
        max_length=255,
        default="ltr",
        help_text="Interessant für bestimmte Sprachen wie Arabisch.",
    )

    subtitle = models.CharField("Untertitel", max_length=255, blank=True)

    feed_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Hauptbild",
        help_text="Wird in Übersichten verwendet.",
    )

    body = StreamField(StandardStreamBlock(), blank=True, verbose_name="Inhalt",)

    search_fields = BasePage.search_fields + [
        index.SearchField("subtitle"),
        index.SearchField("body"),
    ]

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("title", classname="title"),
                FieldPanel("title_color", classname=""),
            ],
            heading="Titel",
        ),
        FieldPanel("subtitle"),
        ImageChooserPanel("feed_image"),
        StreamFieldPanel("body"),
    ]

    promote_panels = [FieldPanel("text_direction"),] + BasePage.promote_panels

    class Meta:
        verbose_name = "Einfache Seite"
        verbose_name_plural = "Einfache Seiten"


@register_snippet
class Banner(models.Model):
    active = models.BooleanField("aktiviert", default=True)
    text = models.CharField("Text", max_length=255)
    button_text = models.CharField("Button-Text", max_length=255, null=True, blank=True)
    button_link = models.URLField("Button-Link", max_length=255, null=True, blank=True)

    panels = [
        FieldPanel("active"),
        FieldPanel("text"),
        FieldPanel("button_text"),
        FieldPanel("button_link"),
    ]

    def __str__(self):
        return self.text


class HomePage(BasePage):
    """
    The HomePage or startpage
    (gets created by a migration)
    """

    is_creatable = False
    og_type = "website"

    search_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Suchmaschinen-Bild",
        help_text="Wird z.B. angezeigt, wenn jmd. www.janun.de bei Facebook postet",
    )

    content = StreamField(HomePageStreamBlock(), blank=True, verbose_name="Inhalt",)

    content_panels = BasePage.content_panels + [StreamFieldPanel("content")]

    promote_panels = BasePage.promote_panels + [ImageChooserPanel("search_image")]

    class Meta:
        verbose_name = "Startseite"

    def get_image(self):
        return self.search_image

    def get_description(self):
        if self.search_description:
            return self.search_description
        return "JANUN ist das Jugendumweltnetzwerk Niedersachsen"


class GroupManager(PageManager):
    def get_queryset(self):
        return super().get_queryset().order_by("title")


class Group(BasePage):
    parent_page_types = ["GroupIndexPage", "Group"]
    subpage_types = ["Project", "StandardPage", "Group"]
    # title is auto added

    subtitle = models.CharField(
        "Untertitel",
        max_length=80,
        null=True,
        blank=True,
        help_text="Z.B. eine sehr kurze Beschreibung",
    )

    body = StreamField(StandardStreamBlock(), blank=True, verbose_name="Inhalt",)

    logo = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Logo",
        # help_text=""
    )

    contact_mail = models.EmailField("E-Mail", null=True, blank=True,)
    contact_name = models.CharField("Name", max_length=255, null=True, blank=True,)
    contact_phone = PhoneNumberField("Telefonnummer", null=True, blank=True,)
    facebook_url = FacebookProfileURLField("Facebook-Profil", null=True, blank=True,)
    website = PrettyURLField("externe Website", null=True, blank=True,)

    address = models.CharField(
        "Adresse",
        help_text="Adresse, an dem die Gruppe zu finden ist",
        max_length=255,
        null=True,
        blank=True,
    )

    list_on_group_index_page = models.BooleanField(
        default="True", verbose_name="Auf Netzwerk & Projekte auflisten?",
    )

    objects = GroupManager()

    search_fields = BasePage.search_fields + [
        index.SearchField("subtitle"),
        index.SearchField("body"),
        index.SearchField("address"),
        index.SearchField("contact_mail"),
        index.SearchField("contact_name"),
        index.SearchField("website"),
    ]

    def get_parent_group(self):
        return Group.objects.parent_of(self).first()

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("subtitle"),
        ImageChooserPanel("logo"),
        FieldPanel("facebook_url"),
        FieldPanel("website"),
        FieldPanel("address"),
        MultiFieldPanel(
            [
                FieldPanel("contact_name"),
                FieldPanel("contact_mail"),
                FieldPanel(
                    "contact_phone", widget=PhoneNumberInternationalFallbackWidget
                ),
            ],
            heading="Kontakt",
        ),
        StreamFieldPanel("body"),
    ]
    promote_panels = [
        FieldPanel("list_on_group_index_page"),
    ]

    settings_panels = None

    partial_template_name = "core/_group.html"

    class Meta:
        verbose_name = "Gruppe"
        verbose_name_plural = "Gruppen"


class Project(Group):
    subpage_types = ["StandardPage", "FormPage"]
    parent_page_types = ["Group"]

    objects = GroupManager()


class GroupIndexPage(BasePage, HeaderMixin):
    # title is auto added
    subpage_types = ["Group", "Project"]
    parent_page_types = ["HomePage"]

    class Meta:
        verbose_name = "Auflistung von Gruppen"

    def get_context(self, request):
        context = super().get_context(request)

        context["groups"] = (
            Group.objects.child_of(self).live().filter(list_on_group_index_page=True)
        )

        country_group = Group.objects.filter(title="JANUN Landesbüro").first()
        if country_group:
            context["countrywide_projects"] = (
                Project.objects.descendant_of(country_group)
                .live()
                .filter(list_on_group_index_page=True)
            )
            context["groups"] = context["groups"].exclude(pk=country_group.pk)
        else:
            context["countrywide_projects"] = []

        context["other_projects"] = (
            Project.objects.descendant_of(self)
            .live()
            .filter(list_on_group_index_page=True)
            .exclude(pk__in=[p.pk for p in context["countrywide_projects"]])
        )

        return context

    content_panels = [
        FieldPanel("title"),
        MultiFieldPanel(HeaderMixin.panels, "Header"),
    ]


class ArticleIndexPage(BasePage):
    """
    lists articles
    """

    subpage_types = ["Article"]
    parent_page_types = ["HomePage"]

    heading = models.CharField("Überschrift", max_length=255)

    content_panels = [
        FieldPanel("title"),
        FieldPanel("heading"),
    ]

    class Meta:
        verbose_name = "Sammlung von Artikeln"

    def get_context(self, request):
        context = super().get_context(request)
        articles = Article.objects.child_of(self).live()
        paginator = Paginator(articles, 20)
        page = request.GET.get("page")
        try:
            articles = paginator.page(page)
        except PageNotAnInteger:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)
        context["articles"] = articles
        return context


class ArticleManager(PageManager):
    def get_queryset(self):
        return super().get_queryset().order_by("-first_published_at")


class Article(FallbackImageMixin, PublishedAtFromGoLiveAtMixin, StandardPage):
    """
    An Article
    """

    parent_page_types = ["ArticleIndexPage"]

    base_form_class = ShortTitleForm

    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Hauptbild",
        help_text="Bild, das den Artikel repräsentiert. Wird in Übersichten verwendet.",
    )

    @property
    def partial_template_name(self):
        return "core/_article.html"

    @property
    def month(self):
        """The 1st of month of the month the article is written in"""
        return datetime.date(
            self.first_published_at.year, self.first_published_at.month, 1
        )

    def get_text(self):
        for block in self.body:
            if block.block_type == "paragraph":
                text = BeautifulSoup(block.value.source, "html5lib").get_text()
                return Truncator(text).words(25)

    related_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        related_name="articles",
        on_delete=models.SET_NULL,
        verbose_name="Zugehörige Gruppe",
        help_text="Eine JANUN-Gruppe, die diesem Artikel zugeordnet ist",
    )

    author = models.ForeignKey(
        "contact.PersonPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pages",
        verbose_name="Autor_in",
    )

    content_panels = [
        MultiFieldPanel(
            [FieldPanel("title", classname="title"), FieldPanel("subtitle"),],
            heading="Titel",
        ),
        FieldPanel("author"),
        FieldPanel("related_group", "core.Group"),
        ImageChooserPanel("main_image"),
        StreamFieldPanel("body"),
    ]

    # promote_panels = [] + StandardPage.promote_panels

    # settings_panels = [] + StandardPage.settings_panels

    objects = ArticleManager()

    class Meta:
        verbose_name = "Artikel"
        verbose_name_plural = "Artikel"


class FormField(AbstractFormField):
    page = ParentalKey("FormPage", related_name="form_fields")


# add validation
class FormPageForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()

        # Make sure confirmation_mail_field really exists in form
        if cleaned_data["send_confirmation_mail"]:
            if not cleaned_data["confirmation_mail_text"]:
                self.add_error(
                    "confirmation_mail_text", "Wird für Bestätigungsmail benötigt"
                )
            if not cleaned_data["confirmation_mail_subject"]:
                self.add_error(
                    "confirmation_mail_subject", "Wird für Bestätigungsmail benötigt"
                )
            if not cleaned_data["confirmation_mail_field"]:
                self.add_error(
                    "confirmation_mail_field", "Wird für Bestätigungsmail benötigt"
                )
            else:
                valid = False
                if "form_fields" in self.formsets:
                    _forms = self.formsets["form_fields"].forms
                    for f in _forms:
                        f.is_valid()
                    for form in _forms:
                        if (
                            form.cleaned_data.get("label")
                            == cleaned_data["confirmation_mail_field"]
                        ):
                            valid = True
                if not valid:
                    self.add_error(
                        "confirmation_mail_field",
                        "Feld '%s' ist im Formular nicht definiert."
                        % cleaned_data["confirmation_mail_field"],
                    )

        return cleaned_data


class FormPage(AbstractEmailForm):
    base_form_class = FormPageForm
    partial_template_name = "core/_partial.html"

    intro = RichTextField(
        blank=True,
        verbose_name="Einführung",
        help_text="Wird über dem Formular angezeigt.",
    )
    thank_you_text = RichTextField(
        blank=True,
        verbose_name="Danke-Text",
        help_text="Wird angezeigt, nachdem das Formular erfolgreich abgesendet wurde.",
    )
    send_confirmation_mail = models.BooleanField(
        default="False",
        verbose_name="Bestätigungsmail versenden?",
        help_text="Soll der Benutzer nach Ausfüllen des Formulars eine Bestätigungsmail bekommen?",
    )
    confirmation_mail_field = models.CharField(
        blank=True,
        verbose_name="Feld für E-Mail-Adresse",
        help_text="Exakte Beschriftung des Felds aus dem Formular für die E-Mail-Adresse des Benutzers. Dahin wird die Bestätigungsmail geschickt.",
        max_length=255,
    )
    confirmation_mail_text = RichTextField(
        blank=True,
        verbose_name="Text",
        help_text="Welcher Text soll in der Bestätigungsmail sein?",
    )
    confirmation_mail_subject = models.CharField(
        blank=True, verbose_name="Betreff", max_length=255
    )

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("intro", classname="full"),
        InlinePanel("form_fields", label="Formular-Felder"),
        FieldPanel("thank_you_text", classname="full"),
        MultiFieldPanel(
            [
                FieldPanel("send_confirmation_mail"),
                FieldPanel("confirmation_mail_field"),
                FieldPanel("confirmation_mail_subject"),
                FieldPanel("confirmation_mail_text", classname="full"),
            ],
            "Bestätigungsmail",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            "Benachrichtigungsmail",
        ),
    ]

    def process_form_submission(self, form):
        submission = super().process_form_submission(form)
        if self.send_confirmation_mail:
            clean_mail_field = str(
                slugify(text_type(unidecode(self.confirmation_mail_field)))
            )
            address = form[clean_mail_field].value()
            html_content = render_to_string(
                "core/mails/form_confirmation.html",
                {
                    "confirmation_mail_text": self.confirmation_mail_text,
                    "title": self.title,
                },
            )
            text_content = html2text.html2text(self.confirmation_mail_text)
            send_mail(
                self.confirmation_mail_subject,
                text_content,
                [address],
                self.from_address,
                html_message=html_content,
            )
        return submission

    class Meta:
        verbose_name = "Formular"
        verbose_name_plural = "Formulare"


class SocialMediaEntry(ClusterableModel):
    link = models.URLField()
    icon_color = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Buntes Icon",
    )
    icon_gray = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Graues Icon",
    )
    tooltip = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("link"),
        FieldPanel("tooltip"),
        ImageChooserPanel("icon_color"),
        ImageChooserPanel("icon_gray"),
    ]

    class Meta:
        abstract = True


class SocialMediaSettingsSocialMediaEntry(Orderable, SocialMediaEntry):
    setting = ParentalKey(
        "core.SocialMediaSettings",
        on_delete=models.CASCADE,
        related_name="social_medias",
    )


@register_setting
class SocialMediaSettings(BaseSetting, ClusterableModel):

    panels = [InlinePanel("social_medias")]

    class Meta:
        verbose_name = "Soziale Medien"
        verbose_name_plural = "Soziale Medien"
