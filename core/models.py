from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

import datetime
from datetime import timedelta

from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import (FieldPanel, InlinePanel,
                                                ObjectList, PageChooserPanel,
                                                StreamFieldPanel, FieldRowPanel,
                                                TabbedInterface, MultiFieldPanel)
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page, PageManager
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from core.fields import FacebookProfileURLField, PrettyURLField
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


from .blocks import StandardStreamBlock, HomePageStreamBlock
from .images import AttributedImage as Image


COLOR_CHOICES = [
    ('green', 'Grün'),
    ('red', 'Rot'),
    ('blue', 'Blau'),
    ('orange', 'Orange'),
]

TEXT_DIRECTION_CHOICES = [
    ('ltr', 'Links nach Rechts'),
    ('rtl', 'Rechts nach Links'),
]


def _(str):
    """dummy trans

    TODO: real translation?
    """
    return str

def stream2text(stream, truncate=False):
    from django.utils.text import Truncator
    import html2text
    h = html2text.HTML2Text()
    h.ignore_links = True
    for block in stream:
        if block.block_type == 'paragraph':
            text = h.handle(block.value.source)
            if truncate:
                return Truncator(text).words(truncate)
            else:
                return text

def stream2image(stream):
    for block in stream:
        if block.block_type == 'image':
            return block.value['image']
        if block.block_type == 'several_images':
            return block.value[0]['image']


class HyphenatedTitleMixin(models.Model):
    """provides hyphenated_title with shy tags"""
    hyphenated_title = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        from softhyphen.html import hyphenate
        self.hyphenated_title = hyphenate(self.title, language="de-de")
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class BasePage(Page, HyphenatedTitleMixin):
    """basic functionality for all our pages"""
    og_type = 'article'
    partial_template_name = 'core/_partial.html'
    medium_partial_template_name = 'core/_medium_partial.html'
    is_creatable = False

    def get_description(self):
        """Short description text for SEO"""
        for attr in ('search_description', 'subtitle', 'role'):
            if hasattr(self, attr) and getattr(self, attr):
                return getattr(self, attr)
        for attr in ('body', 'content', 'text'):
            if hasattr(self, attr) and getattr(self, attr):
                return stream2text(getattr(self, attr), 25)
        if hasattr(type(self)._meta, 'verbose_name'):
            return type(self)._meta.verbose_name
        return ""


    def get_image(self):
        """image for SEO"""
        for attr in ('main_image', 'logo', 'photo', 'header_image'):
            if hasattr(self, attr) and getattr(self, attr):
                return getattr(self, attr)
        for attr in ('body', 'content', 'text'):
            if hasattr(self, attr) and getattr(self, attr):
                return stream2image(getattr(self, attr))
        return None


    def serve_preview(self, request, mode_name):
        request.preview_timestamp = datetime.datetime.now()
        return super(BasePage, self).serve_preview(request, mode_name)



class HighlightManager(models.Manager):
    def active(self):
        return self.get_queryset().filter(
            models.Q(highlighted_page__live=True),
            models.Q(start_datetime__lte=timezone.now()),
            models.Q(end_datetime__isnull=True) |
            models.Q(end_datetime__gt=timezone.now())
        ).order_by('-start_datetime')


def get_in_14_days():
    return timezone.now() + timedelta(days=14)

class Highlight(models.Model):
    """pages can be highlighted
       these can be shown on the homepage for example
       - a time interval can be set, during which the highlight will be shown
       - a custom title can be set, only for the highlighted view
    """
    highlighted_page = ParentalKey(Page, related_name='highlight')
    start_datetime = models.DateTimeField(
        "Startzeit",
        help_text="Ab wann soll das Highlight auftauchen?",
        default=timezone.now
    )
    end_datetime = models.DateTimeField(
        "Endzeit",
        help_text="Bis wann soll das Highlight auftauchen?",
        default=get_in_14_days
    )
    title_override = models.CharField(
        "Überschreib-Titel",
        help_text="Wird statt des Titels des Originals angezeigt.",
        max_length=255,
        blank=True,
    )

    def title():
        doc = "title"
        def fget(self):
            if self.title_override:
                return self.title_override
            else:
                return self.highlighted_page.title
        def fset(self, value):
            self.title_override = value
        def fdel(self):
            del self.title_override
        return locals()
    title = property(**title())

    objects = HighlightManager()


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
                Image.objects.filter(tags__name=self.fallback_image_tag).order_by('?').first()
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
    heading = models.CharField(
        "Überschrift",
        max_length=255,
        blank=True,
    )
    header_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name="Header-Bild",
    )
    panels =  [
        FieldPanel('heading', classname='title'),
        ImageChooserPanel('header_image'),
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
        default='green',
        help_text="Der Titel wird in dieser Farbe angezeigt."
    )

    text_direction = models.CharField(
        "Textrichtung",
        choices=TEXT_DIRECTION_CHOICES,
        max_length=255,
        default='ltr',
        help_text="Interessant für bestimmte Sprachen wie Arabisch."
    )

    subtitle = models.CharField(
        "Untertitel",
        max_length=255,
        blank=True
    )

    feed_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Hauptbild"),
        help_text=_("Wird in Übersichten verwendet.")
    )

    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name=_("Inhalt"),
    )

    search_fields = BasePage.search_fields + [
        index.SearchField('subtitle'),
        index.SearchField('body'),
    ]

    content_panels =  [
        MultiFieldPanel([
            FieldPanel('title', classname='title'),
            FieldPanel('title_color', classname=''),
        ], heading="Titel"),
        FieldPanel('subtitle'),
        ImageChooserPanel('feed_image'),
        StreamFieldPanel('body'),
    ]

    promote_panels = [
        InlinePanel(
            'highlight',
            label=_("Highlight"),
            help_text="""Du kannst diese Seite highlighten.
                         Sie wird dann für den angegeben Zeitraum
                         auf der Startseite angezeigt."""
        ),
        FieldPanel('text_direction'),
    ] + BasePage.promote_panels

    class Meta:
        verbose_name = _("Einfache Seite")
        verbose_name_plural = _("Einfache Seiten")


class HomePage(BasePage):
    """
    The HomePage or startpage
    (gets created by a migration)
    """
    is_creatable = False
    og_type = 'website'

    search_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Suchmaschinen-Bild"),
        help_text=_("Wird z.B. angezeigt, wenn jmd. www.janun.de bei Facebook postet")
    )

    content = StreamField(
        HomePageStreamBlock(),
        blank=True,
        verbose_name=_("Inhalt"),
    )

    content_panels = BasePage.content_panels + [
        StreamFieldPanel('content')
    ]

    promote_panels = BasePage.promote_panels + [
        ImageChooserPanel('search_image')
    ]

    class Meta:
        verbose_name = _("Startseite")

    def get_context(self, request):
        context = super().get_context(request)
        from events.models import EventPage

        highlights = Highlight.objects.active()
        context['highlights'] = highlights[:6]

        upcoming_events = EventPage.objects.upcoming().exclude(
            pk__in=[h.highlighted_page.pk for h in highlights]
        )
        context['upcoming_events'] = upcoming_events[:3]
        context['more_upcoming_events'] = upcoming_events.count() > 3

        articles = Article.objects.live().exclude(
            pk__in=[h.highlighted_page.pk for h in highlights]
        )
        context['articles'] = articles[:3]
        context['more_articles'] = articles.count() > 3
        return context

    def get_image(self):
        return self.search_image

    def get_description(self):
        if self.search_description:
            return self.search_description
        return "JANUN ist das Jugendumweltnetzwerk Niedersachsen"


class GroupManager(PageManager):
    def get_queryset(self):
         return super().get_queryset().order_by('title')

class Group(BasePage):
    parent_page_types = ['GroupIndexPage', 'Group']
    subpage_types = ['Project', 'StandardPage', 'Group']
    # title is auto added

    subtitle = models.CharField("Untertitel",
        max_length=80,
        null=True,
        blank=True,
        help_text="Z.B. eine sehr kurze Beschreibung"
    )

    body = StreamField(
        StandardStreamBlock(),
        blank=True,
        verbose_name=_("Inhalt"),
    )

    logo = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Logo"),
        # help_text=_("")
    )


    contact_mail = models.EmailField(
        "E-Mail",
        null=True,
        blank=True,
    )
    contact_name = models.CharField(
        "Name",
        max_length=255,
        null=True,
        blank=True,
    )
    contact_phone = PhoneNumberField(
        "Telefonnummer",
        null=True,
        blank=True,
    )
    facebook_url = FacebookProfileURLField(
        "Facebook-Profil",
        null=True,
        blank=True,
    )
    website = PrettyURLField(
        "externe Website",
        null=True,
        blank=True,
    )

    address = models.CharField(
        "Adresse",
        help_text="Adresse, an dem die Gruppe zu finden ist",
        max_length=255,
        null=True,
        blank=True,
        # TODO: change this into a real location somehow
    )

    list_on_group_index_page = models.BooleanField(
        default="True",
        verbose_name="Auf Netzwerk & Projekte auflisten?",
    )

    objects = GroupManager()

    search_fields = BasePage.search_fields + [
        index.SearchField('subtitle'),
        index.SearchField('body'),
        index.SearchField('address'),
        index.SearchField('contact_mail'),
        index.SearchField('contact_name'),
        index.SearchField('website'),
    ]

    def get_parent_group(self):
        return Group.objects.parent_of(self).first()

    content_panels = [
            FieldPanel('title', classname="full title"),
            FieldPanel('subtitle'),
            ImageChooserPanel('logo'),
            FieldPanel('facebook_url'),
            FieldPanel('website'),
            FieldPanel('address'),
            MultiFieldPanel([
                FieldPanel('contact_name'),
                FieldPanel('contact_mail'),
                FieldPanel(
                    'contact_phone',
                    widget=PhoneNumberInternationalFallbackWidget
                ),
            ], heading="Kontakt"),
            StreamFieldPanel('body'),
    ]
    promote_panels = [
        FieldPanel('list_on_group_index_page'),
    ]

    settings_panels = None

    partial_template_name = "core/_group.html"

    class Meta:
        verbose_name = _("Gruppe")
        verbose_name_plural = _("Gruppen")


class Project(Group):
    subpage_types = ['StandardPage']
    parent_page_types = ['Group']

    objects = GroupManager()


class GroupIndexPage(BasePage, HeaderMixin):
    # title is auto added
    subpage_types = ['Group', 'Project']
    parent_page_types = ['HomePage']

    class Meta:
        verbose_name = _("Auflistung von Gruppen")

    def get_context(self, request):
        context = super().get_context(request)

        context['groups'] = Group.objects.child_of(self).live().filter(list_on_group_index_page=True)

        country_group = Group.objects.filter(title="JANUN Landesbüro").first()
        if country_group:
            context['countrywide_projects'] = Project.objects.descendant_of(country_group).live().filter(list_on_group_index_page=True)
            context['groups'] = context['groups'].exclude(pk=country_group.pk)
        else:
            context['countrywide_projects'] = []

        context['other_projects'] = Project.objects.descendant_of(self).live().filter(list_on_group_index_page=True).exclude(
            pk__in=[p.pk for p in context['countrywide_projects']]
        )

        return context

    content_panels = [
        FieldPanel('title'),
        MultiFieldPanel(HeaderMixin.panels, "Header"),
    ]


class ArticleIndexPage(BasePage):
    """
    lists articles
    """
    subpage_types = ['Article']
    parent_page_types = ['HomePage']

    class Meta:
        verbose_name = _("Sammlung von Artikeln")

    def get_context(self, request):
        context = super().get_context(request)
        context['articles'] = Article.objects.child_of(self).live()
        return context


class ArticleManager(PageManager):
    def get_queryset(self):
         return super().get_queryset().order_by('-first_published_at')


from .forms import ShortTitleForm

class Article(FallbackImageMixin, PublishedAtFromGoLiveAtMixin, StandardPage):
    """
    An Article
    """
    parent_page_types = ['ArticleIndexPage']

    base_form_class = ShortTitleForm

    main_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name=_("Hauptbild"),
        help_text=_("Bild, das den Artikel repräsentiert. "
                    "Wird in Übersichten verwendet.")
    )

    @property
    def partial_template_name(self):
        return "core/_article.html"

    def get_text(self):
        from bs4 import BeautifulSoup
        from django.utils.text import Truncator
        for block in self.body:
            if block.block_type == 'paragraph':
                text = BeautifulSoup(block.value.source, "html5lib").get_text()
                return Truncator(text).words(25)

    related_group = models.ForeignKey(
        Group,
        null=True,
        blank=True,
        related_name='articles',
        on_delete=models.SET_NULL,
        verbose_name=_("Zugehörige Gruppe"),
        help_text=_("Eine JANUN-Gruppe, die diesem Artikel zugeordnet ist")
    )

    author = models.ForeignKey(
        'contact.PersonPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='pages',
        verbose_name="Autor_in",
    )

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title', classname='title'),
            FieldPanel('title_color', classname=''),
        ], heading="Titel"),
        FieldPanel('subtitle'),
        FieldPanel('author'),
        ImageChooserPanel('main_image'),
        StreamFieldPanel('body'),
    ]

    promote_panels = [
        FieldPanel('related_group', 'core.Group'),
    ] + StandardPage.promote_panels

    settings_panels = [
    ] + StandardPage.settings_panels


    objects = ArticleManager()

    class Meta:
        verbose_name = _("Artikel")
        verbose_name_plural = _("Artikel")




from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel
from wagtail.admin.utils import send_mail
from django.core.exceptions import ValidationError
from wagtail.contrib.forms.forms import WagtailAdminPageForm
from django.utils.text import slugify
from django.utils.six import text_type
from unidecode import unidecode
from django.template.loader import render_to_string



class FormField(AbstractFormField):
    page = ParentalKey('FormPage', related_name='form_fields')


# add validation
class FormPageForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()

        # Make sure confirmation_mail_field really exists in form
        if cleaned_data['send_confirmation_mail']:
            if not cleaned_data['confirmation_mail_text']:
                self.add_error('confirmation_mail_text', 'Wird für Bestätigungsmail benötigt')
            if not cleaned_data['confirmation_mail_subject']:
                self.add_error('confirmation_mail_subject', 'Wird für Bestätigungsmail benötigt')
            if not cleaned_data['confirmation_mail_field']:
                self.add_error('confirmation_mail_field', 'Wird für Bestätigungsmail benötigt')
            else:
                valid = False
                if 'form_fields' in self.formsets:
                    _forms = self.formsets['form_fields'].forms
                    for f in _forms:
                        f.is_valid()
                    for form in _forms:
                        if form.cleaned_data.get('label') == cleaned_data['confirmation_mail_field']:
                            valid = True
                if not valid:
                    self.add_error('confirmation_mail_field', "Feld '%s' ist im Formular nicht definiert." % cleaned_data['confirmation_mail_field'])

        return cleaned_data


class FormPage(AbstractEmailForm):
    base_form_class = FormPageForm
    partial_template_name = 'core/_partial.html'

    intro = RichTextField(
        blank=True,
        verbose_name="Einführung",
        help_text="Wird über dem Formular angezeigt."
    )
    thank_you_text = RichTextField(
        blank=True,
        verbose_name="Danke-Text",
        help_text="Wird angezeigt, nachdem das Formular erfolgreich abgesendet wurde."
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
        max_length=255
    )
    confirmation_mail_text = RichTextField(
        blank=True,
        verbose_name="Text",
        help_text="Welcher Text soll in der Bestätigungsmail sein?"
    )
    confirmation_mail_subject = models.CharField(
        blank=True,
        verbose_name="Betreff",
        max_length=255
    )

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Formular-Felder"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldPanel('send_confirmation_mail'),
            FieldPanel('confirmation_mail_field'),
            FieldPanel('confirmation_mail_subject'),
            FieldPanel('confirmation_mail_text', classname="full"),
        ], "Bestätigungsmail"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Benachrichtigungsmail"),
    ]

    def process_form_submission(self, form):
        submission = super().process_form_submission(form)
        if self.send_confirmation_mail:
            clean_mail_field = str(slugify(text_type(unidecode(self.confirmation_mail_field))))
            address = form[clean_mail_field].value()
            html_content = render_to_string('core/mails/form_confirmation.html', {
                'confirmation_mail_text': self.confirmation_mail_text,
                'title': self.title,
            })
            import html2text
            text_content = html2text.html2text(self.confirmation_mail_text)
            send_mail(
                self.confirmation_mail_subject,
                text_content, [address], self.from_address,
                html_message=html_content)
        return submission

    class Meta:
        verbose_name = _("Formular")
        verbose_name_plural = _("Formulare")
