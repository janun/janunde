from django import forms
from core.models import Group

from form_utils.forms import BetterForm

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget



class SeminarForm(BetterForm):

    def __init__(self, *args, **kwargs):
        richtlinie = kwargs.pop('richtlinie', None)
        datenschutz = kwargs.pop('richtlinie', None)
        super().__init__(*args, **kwargs)
        if richtlinie:
            self.fields['read_richtlinie'].label = self.fields['read_richtlinie'].label.replace(
                "Seminarabrechnungsrichtlinie",
                "<a href=\"%s\">Seminarabrechnungsrichtlinie</a>" % richtlinie.url
            )
        if datenschutz:
            self.fields['read_datenschutz'].label = self.fields['read_datenschutz'].label.replace(
                "Datenschutzbedingungen",
                "<a href=\"%s\">Datenschutzbedingungen</a>" % datenschutz.url
            )

    class Meta:
        fieldsets = [
            ('Allgemeines zu Deinem Seminar', {
                'fields': ['title', 'subtitle', 'begin', 'end', 'location', 'description'],
            }),
            ('Daten zur Förderungshöhe', {
                'fields': ['days', 'attendees', 'group', 'requested'],
            }),
            ('Kontakt zu Dir', {
                'description': "Damit wir Dich zu Deinem Seminar kontaktieren können.",
                'fields': ['contact_name', 'contact_mail', 'contact_phone'],
            }),
            ('Veröffentlichung auf der JANUN-Website', {
                'description': "Wir würden Dein Seminar gerne auf der JANUN-Website bewerben.",
                'fields': ['publish', 'image', 'image_copyright'],
            }),
            ('Kontaktdaten auf der JANUN-Website', {
                'description': "Damit Interessierte auf der JANUN-Website jmd. kontaktieren können",
                'fields': ['website_contact_name', 'website_contact_mail', 'website_contact_phone'],
            }),
            ('footer', {
                'legend': '',
                'fields': ['comments', 'read_richtlinie', 'read_datenschutz', 'really_antrag', 'read_deadlines'],
            }),
        ]

    title = forms.CharField(
        label='Titel', max_length=50,
        widget=forms.TextInput(attrs={'class': "form__input--full"}),
        help_text="Beschreib oder bennene Dein Seminar in max. 50 Zeichen."
    )
    subtitle = forms.CharField(
        label='Untertitel', max_length=100, required=False,
        widget=forms.TextInput(attrs={'style': "width:100%"}),
        help_text="Gib, falls nötig, noch mehr Infos in weiteren max. 100 Zeichen."
    )

    begin = forms.SplitDateTimeField(label='Beginn')

    end = forms.SplitDateTimeField(label='Ende')

    location = forms.CharField(
        label='Ort', help_text="Wo findet das Seminar statt? Bsp.: <em>Jugendumweltbüro, Goebenstr. 3a, 30161 Hannover</em>",
        widget=forms.TextInput(attrs={'class': "form__input--full"})
    )

    description = forms.CharField(
        label='Beschreibung', widget=forms.Textarea(attrs={'style': "width:100%"}),
        help_text="Um was genau geht es bei Deinem Seminar?"
    )

    # TODO: Fill in using jquery?
    days = forms.IntegerField(
        label='Bildungstage',
        help_text="Wieviele Bildungstage enthält Dein Seminar?",
        min_value=1
    )

    # TODO: Rangefield
    attendees = forms.IntegerField(
        label='Anzahl Teilnehmer_innen',
        help_text="Wieviele Teilnehmer_innen erwartest Du?",
        min_value=1
    )

    requested = forms.DecimalField(
        label='benötigte Summe',
        help_text="Wieviel Förderung wirst du voraussichtlich abrufen?",
        min_value=1,
        decimal_places=2
    )

    group = forms.ModelChoiceField(
        label='JANUN-Gruppe', required=False,
        queryset=Group.objects.all(),
        empty_label="als Einzelperson anmelden",
        help_text="Du kannst ein Seminar als <em>Einzelperson</em> oder für eine <em>JANUN-Gruppe</em> anmelden.",
        widget=forms.Select(attrs={'class': "form__input--full"})
    )

    contact_name = forms.CharField(
        label='Name', widget=forms.TextInput(attrs={'class': "form__input--full"}),
    )
    contact_mail = forms.EmailField(
        label='E-Mail-Adresse',
        # help_text="Auch. Und, nein, wir verschicken natürlich kein Spam.",
        widget=forms.EmailInput(attrs={'size': 25}),
    )
    contact_phone = PhoneNumberField(
        label='Telefonnummer', required=False,
        # help_text="Ebenfalls.",
        widget=PhoneNumberInternationalFallbackWidget()
    )

    publish = forms.BooleanField(
        label='veröffentlichen?',
        initial=True, required=False
    )

    image = forms.ImageField(
        label='Bild',
        required=False,
        widget=forms.FileInput(attrs={'accept': "image/*"})
    )

    # TODO: validate must be present if image is present
    # TODO: ComboField for image and copyright
    image_copyright = forms.CharField(
        label="Urheberecht des Bildes",
        help_text="Wo liegt das Urheberecht des Bildes? Bsp.: <em>pixabay</em> oder Name der Fotografin",
        required=False
    )

    website_contact_name = forms.CharField(
        label='Name', widget=forms.TextInput(attrs={'class': "form__input--full"}),
        required=False,
    )
    website_contact_mail = forms.EmailField(
        label='E-Mail-Adresse',
        widget=forms.EmailInput(attrs={'size': 25}),
        required=False,
    )
    website_contact_phone = PhoneNumberField(
        label='Telefonnummer', required=False,
        widget=PhoneNumberInternationalFallbackWidget()
    )

    comments = forms.CharField(
        label='Anmerkungen', widget=forms.Textarea(attrs={'style': "width:100%"}),
        help_text="Gibt es noch etwas, das Du uns mitteilen willst?",
        required=False
    )

    # TODO: Link to Richtlinie
    read_richtlinie = forms.BooleanField(
        label="Ich habe die Seminarabrechnungsrichtlinie gelesen und verstanden, unter welchen Bedingungen JANUN Seminare bezuschusst."
    )
    read_datenschutz = forms.BooleanField(
        label="Ich habe die Datenschutzbedingungen gelesen und verstanden."
    )
    really_antrag = forms.BooleanField(
        label="Die maximale Bezuschussung <span id=\"checkPossibleFunding\"></span> möchte ich hiermit beantragen."
    )
    read_deadlines = forms.BooleanField(
        label="Ich habe mich über die Abrechnungsdeadlines bei JANUN informiert (<span id=\"deadline\">15. Januar, 15. April, 15. Juli, 15. Oktober</span>) zu denen die kompletten Seminarabrechnungen bei euch eingegangen sein müssen."
    )
