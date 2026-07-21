from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
import random
import string
from django.utils import timezone
from django.core.validators import RegexValidator

LANGUAGE_CHOICES = (
    ('pl', 'Polish'),
    ('en', 'English'),
)

class Host(models.Model):
    host_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=9)
    email = models.EmailField(blank=True, default='')

    def __str__(self):
        return self.host_name


class Company(models.Model):
    company_name = models.CharField(max_length=100)
    host_name = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.company_name

class Visitor(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=9, null=True)

    # ⬇️ FK do Company — usuń proszę ten default="Brak" (to niepoprawne dla FK)
    factory = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    # ⬇️ NAJWAŻNIEJSZE: tekstowa nazwa firmy wpisana „z palca”
    company_name_text = models.CharField(max_length=255, blank=True, default="")

    visit_purpose = models.TextField(null=False)
    host = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True, blank=True)
    visitor_id = models.CharField(max_length=20, validators=[RegexValidator(r'^\d{1,20}$', 'ID musi składać się z cyfr.')], null=False)
    production_area = models.BooleanField()
    with_supervision = models.BooleanField(default=True, blank=True)
    safety_acknowledged = models.BooleanField(default=False)
    signed = models.ImageField(upload_to='signatures/')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    audit_start_date = models.DateField(null=True, blank=True)
    audit_end_date = models.DateField(null=True, blank=True)
    badge_returned = models.BooleanField(default=False)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='pl')
    safety_question_1 = models.CharField(max_length=500, blank=True, null=True)
    safety_question_2 = models.CharField(max_length=500, blank=True, null=True)
    safety_question_3 = models.CharField(max_length=500, blank=True, null=True)
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_visits')
    known_guest = models.BooleanField(default=False)
    returned_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='returned_visits')
    reservation = models.OneToOneField(
        'GuestBook.Reservation',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='visitor'
    )

    SMS_CHOICES = [
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("timeout", "Timeout"),
        ("error", "Error"),
        ("skipped", "Skipped"),
    ]
    PRINT_CHOICES = [
        ("pending", "Pending"),
        ("printed", "Printed"),
        ("timeout", "Timeout"),
        ("error", "Error"),
        ("skipped", "Skipped"),
    ]
    sms_status = models.CharField(max_length=16, choices=SMS_CHOICES, default="pending")
    print_status = models.CharField(max_length=16, choices=PRINT_CHOICES, default="pending")
    id_issued = models.BooleanField(default=False)  # czy karta została wydana przez recepcję

    def is_present(self):
        return self.end_time is None or not self.badge_returned

    @property
    def company_display(self) -> str:
        """Priorytet: wybrana firma z listy → tekst ręczny → 'Brak'."""
        if self.factory:
            return self.factory.company_name
        return self.company_name_text or "No company"

class TrustedVisitor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=9)
    company = models.CharField(max_length=100, blank=True)
    visit_purpose = models.TextField()
    host_name = models.CharField(max_length=100)
    host_phone = models.CharField(max_length=9)
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='pl')
    production_area = models.BooleanField(default=False)
    with_supervision = models.BooleanField(default=False)
    safety_acknowledged = models.BooleanField(default=True)
    badge_id = models.CharField(max_length=50, unique=True)  # identyfikator/pestka

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.badge_id})"


class AdminProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, default="-")
    last_name = models.CharField(max_length=100, default="-")
    email = models.EmailField(max_length=100, default="-")
    signature = models.ImageField(upload_to='admin_signatures/', blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    printer_address = models.CharField(max_length=200, blank=True, default='10.30.40.150', verbose_name='Printer IP/hostname')
    printer_port = models.IntegerField(default=9100, verbose_name='Printer port')


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    visitor_first_name = models.CharField(max_length=100)
    visitor_last_name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)
    host = models.ForeignKey(Host, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=9)

    visit_purpose_choice = models.CharField(max_length=100, blank=True)
    other_purpose = models.CharField(max_length=255, blank=True, null=True)
    audit_start_date = models.DateField(null=True, blank=True)
    audit_end_date = models.DateField(null=True, blank=True)

    factory = models.BooleanField(default=False)
    supervision = models.BooleanField(default=False)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    conference_needed = models.BooleanField(default=False)
    conference_room = models.CharField(
        max_length=50,
        choices=[
            ("VIP", "VIP"),
            ("Kreatywna", "Kreatywna"),
            ("Kameralna", "Kameralna")
        ],
        blank=True,
        null=True
    )

    STATUS_CHOICES = [
        ('sent', 'Reservation Sent'),
        ('arrived', 'Arrived'),
        ('completed', 'Visit Completed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default='sent'
        )

    sms_status = models.CharField(
        max_length=16,
        choices=[
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('timeout', 'Timeout'),
            ('error', 'Error'),
            ('no_number', 'No number'),
            ('skipped', 'Skipped'),
        ],
        default='pending',
        blank=True,
    )
    cancelled_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.visitor_first_name} {self.visitor_last_name} ({self.date})"

class ReservationCode(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    usage_count = models.PositiveIntegerField(default=0)  # ile razy już użyto
    max_uses = models.PositiveIntegerField(default=3)     # limit użyć
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join(random.choices(string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Code {self.code} for {self.reservation}"

    def can_use(self) -> bool:
        """Czy kod może być jeszcze użyty?"""
        return self.usage_count < self.max_uses

    def register_use(self) -> bool:
        """
        Zwiększa licznik użyć, jeśli jeszcze można.
        Zwraca True jeśli się udało, False jeśli limit przekroczony.
        """
        if self.can_use():
            self.usage_count += 1
            self.save(update_fields=['usage_count'])
            return True
        return False



from django.conf import settings
from django.db import models
from django.utils import timezone

class Sender(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Recipient(models.Model):
    """Aktualizuje tylko helpdesk; można dodać pola kontaktowe do maila."""
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, default="", db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class KioskSettings(models.Model):
    """Singleton model for kiosk-wide settings (printer etc.)."""
    printer_address = models.CharField(max_length=200, default='10.30.40.150')
    printer_port = models.IntegerField(default=9100)

    class Meta:
        verbose_name = 'Kiosk Settings'

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Package(models.Model):
    class Status(models.TextChoices):
        IN_BOX = "in_box", "W paczkomacie"
        ISSUED = "issued", "Wydana"

    delivered_at = models.DateTimeField("Delivered at", default=timezone.now)

    # teraz FK zamiast czystego tekstu
    sender = models.ForeignKey(Sender, on_delete=models.PROTECT, related_name="packages")
    recipient = models.ForeignKey(Recipient, on_delete=models.PROTECT, related_name="packages")

    code = models.CharField("Code", max_length=32, unique=True, db_index=True)
    label_code = models.CharField("Package number (from label)", max_length=64, blank=True, default="")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.IN_BOX)

    staff_comment = models.TextField("Reception comment", blank=True, default="")
    label_photo = models.ImageField(upload_to="package_labels/", null=True, blank=True)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="+")

    collected_by = models.ForeignKey(
        Recipient, null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )
    collected_by_name = models.CharField(max_length=150, blank=True)

    phone_number = models.CharField("Phone number", max_length=30, blank=True, default="")

    issued_at = models.DateTimeField(null=True, blank=True)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name="+")
    # ślad zmian (kto edytował)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="edit")

    def __str__(self):
        return f"{self.code} → {self.recipient} ({self.get_status_display()})"

