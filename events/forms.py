from django import forms
from core.models import Group
from core.widgets import SplitDateTimeWidget

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


funny_placeholders = [
    {
        'title': "z.B. Einhorn-Dressurschule",
        'location': "z.B. Einhorn-Dressurschule, Einhornstraße 8, 30161 Hannover",
        'description': "z.B. Bei der Einhorn-Dressurschule lernst Du Dein Einhorn zu dressieren",
        'begin': "z.B. 26.10.2017 10 Uhr",
        'end': "z.B. 27.10.2017 20 Uhr",
        'name': "z.B. Max Mustermann",
        'mail': "z.B. max.mustermann@gmx.net"
    }
]


# class DateOrTimeInput():
#     pass

class SeminarForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for key, value in funny_placeholders[0].items():
        #     self.fields[key].widget.attrs['placeholder'] = value

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

    begin = forms.SplitDateTimeField(
        label='Beginn', widget=SplitDateTimeWidget()
    )

    end = forms.SplitDateTimeField(
        label='Ende', widget=SplitDateTimeWidget()
    )

    # TODO: Fill in using jquery?
    days = forms.IntegerField(
        label='Bildungstage',
        help_text="Wieviele Tage Deines Seminars haben min. 6 Stunden Bildungsarbeit?",
        min_value=1
    )

    location = forms.CharField(
        label='Ort', help_text="Wo findet das Seminar statt? Bsp.: <em>UJZ Korn, Kornstraße 28, 30167 Hannover</em>",
        widget=forms.TextInput(attrs={'class': "form__input--full"})
    )

    description = forms.CharField(
        label='Beschreibung', widget=forms.Textarea(attrs={'style': "width:100%"}),
        help_text="Um was genau geht es bei Deinem Seminar?"
    )

    attendees = forms.IntegerField(
        label='Anzahl Teilnehmer_innen',
        help_text="Wieviele Teilnehmer_innen erwartest Du?",
        min_value=1
    )

    group = forms.ModelChoiceField(
        label='JANUN-Gruppe', required=False,
        queryset=Group.objects.all(),
        empty_label="als Einzelperson anmelden",
        help_text="Du kannst ein Seminar als <em>Einzelperson</em> oder für eine <em>JANUN-Gruppe</em> anmelden.",
        widget=forms.Select(attrs={'class': "form__input--full"})
    )

    contact_name = forms.CharField(
        label='Dein Name', widget=forms.TextInput(attrs={'class': "form__input--full"}),
        help_text="Damit wir Dich zu Deinem Seminar kontaktieren können.",
    )
    contact_mail = forms.EmailField(
        label='Deine E-Mail-Adresse',
        # help_text="Auch. Und, nein, wir verschicken natürlich kein Spam.",
        widget=forms.EmailInput(attrs={'size': 25}),
    )
    contact_phone = PhoneNumberField(
        label='Deine Telefonnummer', required=False,
        # help_text="Ebenfalls.",
        widget=PhoneNumberInternationalFallbackWidget()
    )

    publish = forms.BooleanField(
        label='Auf janun.de veröffentlichen?',
        help_text="Wir würden Dein Seminar gerne auf der JANUN-Website bewerben.",
        initial=True, required=False
    )

    image = forms.ImageField(
        label='Bild',
        help_text="Benutzen wir auf janun.de, um Dein Seminar zu bewerben.",
        required=False,
        widget=forms.FileInput(attrs={'accept': "image/*"})
    )

    comments = forms.CharField(
        label='Anmerkungen', widget=forms.Textarea(attrs={'style': "width:100%"}),
        help_text="Gibt es noch etwas, das Du uns mitteilen willst?",
        required=False
    )
