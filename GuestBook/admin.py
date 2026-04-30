from django.contrib import admin
from .models import Visitor, TrustedVisitor, AdminProfile, Reservation, ReservationCode, Host, Company
from django.contrib.admin import SimpleListFilter
from django.db.models import F
from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Package, Sender, Recipient


@admin.register(Host)
class HostAdmin(admin.ModelAdmin):
    list_display = ('host_name', 'phone')
    search_fields = ('host_name', 'phone')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'host_name')
    search_fields = ('company_name', 'host_name')


@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'visitor_id',
        'get_host_name', 'get_host_phone',
        'production_area', 'with_supervision',
        'safety_acknowledged', 'is_present',
        'start_time', 'end_time', 'badge_returned', 'approved', 'known_guest'
    )
    list_filter = (
        'production_area', 'with_supervision', 'safety_acknowledged',
        'badge_returned', 'approved', 'known_guest', 'language'
    )
    search_fields = ('first_name', 'last_name', 'visitor_id', 'host__host_name')
    readonly_fields = ('start_time', 'end_time', 'signed', 'approved_by', 'returned_by')
    ordering = ('-start_time',)

    def get_host_name(self, obj):
        return obj.host.host_name if obj.host else "-"
    get_host_name.short_description = "Host Name"

    def get_host_phone(self, obj):
        return obj.host.phone if obj.host else "-"
    get_host_phone.short_description = "Host Phone"


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'phone_number')
    readonly_fields = ('user', 'first_name', 'last_name', 'email', 'signature')


@admin.register(TrustedVisitor)
class TrustedVisitorAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'badge_id', 'company',
        'host_name', 'host_phone', 'language', 'production_area'
    )
    list_filter = ('language', 'production_area', 'with_supervision')
    search_fields = ('first_name', 'last_name', 'badge_id', 'host_name')


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'visitor_first_name', 'visitor_last_name', 'date', 'time', 'conference_room',
        'factory', 'supervision', 'conference_needed'
    )
    list_filter = ('date', 'conference_room', 'factory', 'supervision', 'conference_needed')
    search_fields = ('visitor_first_name', 'visitor_last_name', 'company', 'phone')


class ExhaustedFilter(SimpleListFilter):
    title = "Exhausted"
    parameter_name = "exhausted"

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if val == 'yes':
            return queryset.filter(usage_count__gte=F('max_uses'))
        if val == 'no':
            return queryset.filter(usage_count__lt=F('max_uses'))
        return queryset

@admin.register(ReservationCode)
class ReservationCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'reservation',
        'usage_count',
        'max_uses',
        'uses_left',
        'is_exhausted',
        'created_at',
    )
    list_filter = (ExhaustedFilter, 'created_at')
    search_fields = ('code', 'reservation__visitor_first_name', 'reservation__visitor_last_name')
    readonly_fields = ('code', 'created_at')

    @admin.display(description="Uses left")
    def uses_left(self, obj: ReservationCode):
        return max(obj.max_uses - obj.usage_count, 0)

    @admin.display(boolean=True, description="Exhausted")
    def is_exhausted(self, obj: ReservationCode):
        return obj.usage_count >= obj.max_uses

HELPDESK_GROUPS = {"GuestBook_Helpdesk", "SupportCenter"}

def is_helpdesk(user) -> bool:
    return user.is_superuser or user.groups.filter(name__in=HELPDESK_GROUPS).exists()


# ---- Sender ----



# ---- Filtr statusu z szybkimi skrótami ----
class PackageStatusFilter(admin.SimpleListFilter):
    title = _("Status")
    parameter_name = "status"

    def lookups(self, request, model_admin):
        return [
            (Package.Status.IN_BOX, _("In box")),
            (Package.Status.ISSUED, _("Issued")),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


# ---- Package ----
@admin.register(Sender)
class SenderAdmin(admin.ModelAdmin):
    list_display = ("name", "packages_count")
    search_fields = ("name",)

    def packages_count(self, obj):
        return obj.packages.count()
    packages_count.short_description = "Packages"


# ---- Recipient (zarządzany przez Helpdesk) ----
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "packages_in_box", "packages_issued")
    search_fields = ("name", "email")

    def has_add_permission(self, request):
        return is_helpdesk(request.user)

    def has_change_permission(self, request, obj=None):
        return is_helpdesk(request.user)

    def has_delete_permission(self, request, obj=None):
        return is_helpdesk(request.user)

    def packages_in_box(self, obj):
        return obj.packages.filter(status=Package.Status.IN_BOX).count()
    packages_in_box.short_description = "In box"

    def packages_issued(self, obj):
        return obj.packages.filter(status=Package.Status.ISSUED).count()
    packages_issued.short_description = "Issued"


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "code", "sender", "recipient", "status_badge",
        "delivered_at", "issued_at", "issued_by",
        "collected_by_display",
    )
    list_filter = (PackageStatusFilter, "sender", "recipient", "delivered_at", "issued_at")
    date_hierarchy = "delivered_at"
    search_fields = ("code", "sender__name", "recipient__name", "collected_by_name")
    autocomplete_fields = ("sender", "recipient", "collected_by", "created_by", "issued_by", "updated_by")
    readonly_fields = ("code", "created_at", "created_by", "issued_at", "issued_by", "updated_at", "updated_by")
    actions = ("reprint_label",)

    fieldsets = (
        (_("Basic"), {
            "fields": ("code", "status", "delivered_at", "sender", "recipient")
        }),
        (_("Issuing"), {
            "fields": ("issued_at", "issued_by", "collected_by", "collected_by_name")
        }),
        (_("Meta"), {
            "classes": ("collapse",),
            "fields": ("created_at", "created_by", "updated_at", "updated_by"),
        }),
    )

    # ładna plakietka statusu
    def status_badge(self, obj):
        color = "#ffc107; color:#212529" if obj.status == Package.Status.IN_BOX else "#198754; color:white"
        return format_html('<span style="padding:2px 8px;border-radius:12px;background:{}">{}</span>',
                           color, obj.get_status_display())
    status_badge.short_description = "Status"
    status_badge.admin_order_field = "status"

    def collected_by_display(self, obj):
        return obj.collected_by.name if obj.collected_by else (obj.collected_by_name or "—")
    collected_by_display.short_description = "Collected by"

    # akcja: ponowny wydruk etykiety
    def reprint_label(self, request, queryset):
        ok_count = 0
        err_count = 0
        for pkg in queryset:
            try:
                zpl = render_box_label_from_file(pkg.code, pkg.sender.name, pkg.recipient.name)
                ok, err = send_zpl_to_printer(zpl)
                if ok:
                    ok_count += 1
                else:
                    err_count += 1
            except Exception:
                err_count += 1
        if ok_count:
            messages.success(request, _(f"Ponownie wydrukowano etykiety: {ok_count}"))
        if err_count:
            messages.warning(request, _(f"Nieudane wydruki: {err_count}"))
    reprint_label.short_description = "Reprint label for selected"
