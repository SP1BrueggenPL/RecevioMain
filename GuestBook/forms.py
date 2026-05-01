from django import forms
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserLoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'id': 'floatingInput', 'class': 'form-control mb-3'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'floatingPassword', 'class': 'form-control mb-3'}), required=True)

    class Meta:
        model = User
        fields = ['username','password']

VISIT_PURPOSE_CHOICES_ORIGINAL = [
    ('', '--- Select ---'),
    ('Job interview', 'Job interview'),
    ('audit', 'Audit'),
    ('Business meeting with partners or contractors', 'Business meeting with partners or contractors'),
    ('Strategic meeting', 'Strategic meeting'),
    ('Training session', 'Training session'),
    ('Service or maintenance visit', 'Service or maintenance visit'),
    ('Educational or school visit', 'Educational or school visit'),
    ('other', 'Other purpose'),
]


VISIT_PURPOSE_CHOICES = [
    ('--- Select ---', '--- Select ---'),
    ('Job interview', _('Job interview')),
    ('audit', _('Audit')),
    ('Business meeting with partners or contractors', _('Business meeting with partners or contractors')),
    ('Strategic meeting', _('Strategic meeting')),
    ('Training session', _('Training session')),
    ('Service or maintenance visit', _('Service or maintenance visit')),
    ('Educational or school visit', _('Educational or school visit')),
    ('other', _('Other purpose')),
]

class VisitorForm(forms.ModelForm):
    visit_purpose_choice = forms.ChoiceField(
        choices=VISIT_PURPOSE_CHOICES,
        required=False,
        label=_("Purpose of Visit")
    )

    other_purpose = forms.CharField(
        required=False,
        label=_("Other purpose"),
        widget=forms.TextInput(attrs={'placeholder': _('Enter custom purpose')})
    )

    audit_start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=_("Audit Start Date")
    )

    audit_end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=_("Audit End Date")
    )

    other_company = forms.CharField(
        required=False,
        label=_("Other company (if not listed)")
    )

    no_company = forms.BooleanField(
        required=False,
        label=_("I do not represent any company")
    )

    class Meta:
        model = Visitor
        fields = ['first_name', 'last_name', 'phone', 'factory', 'host']
        labels = {
            'first_name': _("First name"),
            'last_name': _("Last name"),
            'phone': _("Phone"),
            'factory': _("Factory"),
            'host': _("Host"),
        }

    def clean(self):
        cleaned_data = super().clean()
        factory = cleaned_data.get('factory')
        other_company = cleaned_data.get('other_company')
        no_company = cleaned_data.get('no_company')

        if not factory and not no_company and not other_company:
            raise forms.ValidationError(_("Please select a company, enter one manually, or check 'no company'."))

        # jeśli wybrano firmę z listy, a jednocześnie wpisano „inną" — utnij „inną"
        if factory and other_company:
            cleaned_data['other_company'] = ""

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'autocomplete': 'off'})


class SignatureForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['signed']
        labels = {
            'signed': _('Signed'),
        }

class SafetyForm(forms.Form):
    accepted = forms.BooleanField(label="Zapoznałem/am się z zasadami BHP")

class SupervisionForm(forms.Form):
    with_supervision = forms.ChoiceField(
        choices=[(True, 'Z opieką'), (False, 'Bez opieki')],
        widget=forms.RadioSelect, label="Czy przebywasz z opieką?"
    )

class ProductionForm(forms.Form):
    production_area = forms.ChoiceField(
        choices=[(True, 'Tak'), (False, 'Nie')],
        widget=forms.RadioSelect, label="Czy będziesz przebywać na obszarze produkcji?"
    )
class ReservationForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('sent', _('Reservation Sent')),
        ('arrived', _('Arrived')),
        ('completed', _('Visit Completed')),
    ]

    visit_purpose_choice = forms.ChoiceField(
        required=False,
        label=_("Purpose of Visit"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    other_purpose = forms.CharField(
        required=False,
        label=_("Other Purpose"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    audit_start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label=_("Audit Start Date")
    )

    audit_end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label=_("Audit End Date")
    )

    other_company = forms.CharField(
        required=False,
        label=_("Other company (if not listed)"),
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    no_company = forms.BooleanField(
        required=False,
        label=_("I do not represent any company.")
    )

    class Meta:
        model = Reservation
        fields = [
            'visitor_first_name', 'visitor_last_name', 'phone',
            'company', 'host',
            'visit_purpose_choice', 'other_purpose', 'audit_start_date', 'audit_end_date',
            'factory', 'supervision', 'date', 'time',
            'conference_needed', 'conference_room'
        ]
        widgets = {
            'company': forms.Select(attrs={'class': 'form-control'}),
            'host': forms.Select(attrs={'class': 'form-control'}),
            'visitor_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'visitor_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'conference_needed': forms.CheckboxInput(),
            'conference_room': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        disable_translation = kwargs.pop("disable_translation", False)
        super().__init__(*args, **kwargs)

        # ✅ choices ustawiamy dopiero teraz
        self.fields["visit_purpose_choice"].choices = (
            VISIT_PURPOSE_CHOICES_ORIGINAL if disable_translation else VISIT_PURPOSE_CHOICES
        )

    def clean(self):
        cleaned_data = super().clean()
        company = cleaned_data.get('company')
        other_company = cleaned_data.get('other_company')
        no_company = cleaned_data.get('no_company')

        if not company and not other_company and not no_company:
            raise forms.ValidationError(
                _("Please select a company, type one or confirm you don't represent any.")
            )
        return cleaned_data


class BadgeIDForm(forms.Form):
    badge_id = forms.CharField(
        label=_("Enter your badge ID"),
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg text-center', 'placeholder': _('Badge ID')})
    )


from django import forms
from .models import Package, Sender, Recipient
from django.utils import timezone

class LabelScanForm(forms.Form):
    label_image = forms.ImageField(
        label="Zdjęcie etykiety",
        widget=forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"})
    )


class PackageForm(forms.ModelForm):
    # 1) Nadawca: wybór z listy **lub** wpisanie nowego
    sender = forms.ModelChoiceField(
        queryset=Sender.objects.all(),
        required=False,
        empty_label="----------",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    new_sender = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nowy nadawca (jeśli brak na liście)"})
    )

    # 2) Odbiorca: tylko z listy (zarządzany przez helpdesk)
    recipient = forms.ModelChoiceField(
        queryset=Recipient.objects.all(),
        required=True,
        empty_label="----------",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    delivered_at = forms.DateTimeField(
        initial=timezone.now,
        widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"})
    )

    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Numer telefonu nadawcy"})
    )

    class Meta:
        model = Package
        fields = ["delivered_at", "sender", "new_sender", "phone_number", "recipient"]

    def clean(self):
        data = super().clean()
        sender = data.get("sender")
        new_sender = (data.get("new_sender") or "").strip()

        if not sender and not new_sender:
            raise forms.ValidationError("Wybierz nadawcę z listy albo wpisz nowego.")
        if sender and new_sender:
            raise forms.ValidationError("Podaj tylko jedną opcję nadawcy.")
        return data

    def save(self, commit=True, user=None):
        obj = super().save(commit=False)

        # tworzenie nowego nadawcy, jeśli podano
        if not self.cleaned_data["sender"]:
            s, _ = Sender.objects.get_or_create(name=self.cleaned_data["new_sender"])
            obj.sender = s

        if user and not obj.pk:
            obj.created_by = user
        if commit:
            obj.save()
        return obj


# forms.py
from django import forms
from django.utils.translation import gettext_lazy as _

class ScanForm(forms.Form):
    code = forms.CharField(
        label=_("Package code"),
        max_length=32,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "autofocus": "autofocus",
            "autocomplete": "off",
            "placeholder": _("Skan or write code…"),
        }),
    )
    # było: queryset=Host.objects.all()
    collected_by = forms.ModelChoiceField(
        label=_("Recipient"),
        queryset=Recipient.objects.order_by("name"),   # ← TU ZMIANA
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


    def __init__(self, *args, **kwargs):
        self.confirm = kwargs.pop("confirm", False)
        super().__init__(*args, **kwargs)

    def clean(self):
        c = super().clean()
        if self.confirm:
            if not c.get("collected_by") and not (c.get("collected_by_other") or "").strip():
                raise forms.ValidationError(_("Please provide the name of the recipient"))
        return c


# HELPDESK – proste formularze zarządzania
class SenderForm(forms.ModelForm):
    class Meta:
        model = Sender
        fields = ["name"]
        widgets = {"name": forms.TextInput(attrs={"class": "form-control"})}


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["name", "email"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }


class PackageEditForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ["delivered_at", "sender", "recipient"]
        widgets = {
            "delivered_at": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}),
            "sender": forms.Select(attrs={"class": "form-select"}),
            "recipient": forms.Select(attrs={"class": "form-select"}),
        }
