from ldap3 import Server, Connection, NONE, SUBTREE
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group
from django.conf import settings
from .models import AdminProfile

LDAP_CONNECT_TIMEOUT = 5   # seconds to establish TCP connection
LDAP_RECEIVE_TIMEOUT = 10  # seconds to wait for LDAP response


class ChipPinBackend:
    """Staff login via a 5-digit chip number + a 6-digit authorization code
    (PIN) the user sets on first login — see AdminProfile.chip_number/pin_hash
    and the `login` view in views.py. Only matches when called with
    chip_number/pin kwargs, so it doesn't interfere with ModelBackend's
    username/password calls (e.g. the Django admin login at /nimda/)."""

    def authenticate(self, request, chip_number=None, pin=None, **kwargs):
        if not chip_number or not pin:
            return None
        profile = AdminProfile.objects.select_related('user').filter(chip_number=chip_number).first()
        if not profile or not profile.pin_hash:
            return None
        if not profile.user.is_active:
            return None
        if not check_password(pin, profile.pin_hash):
            return None
        return profile.user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if user.is_active else None


class LDAPBackend:
    def authenticate(self, request, username=None, password=None):
        ldap_server = settings.LDAP_SERVER_URI
        if not ldap_server:
            print("[LDAP] ❌ LDAP_SERVER_URI nie jest ustawiony — pomijam backend LDAP")
            return None
        ldap_base_dn = settings.LDAP_USER_BASE_DN or "DC=brueggen,DC=com"
        server = Server(ldap_server, get_info=NONE, connect_timeout=LDAP_CONNECT_TIMEOUT)

        # User DN do logowania
        user_dn = f"{username}@{settings.LDAP_DOMAIN}"

        print(f"[LDAP] ✅ Próba logowania: {username}")
        print(f"[LDAP] ✅ Loguję się jako: {user_dn}")
        print(f"[LDAP] ✅ Przeszukuję katalog: {ldap_base_dn}")

        try:
            # Logujemy się jako użytkownik serwisowy
            service_conn = Connection(
                server,
                user=settings.LDAP_BIND_DN,
                password=settings.LDAP_BIND_PASSWORD,
                auto_bind=True,
                receive_timeout=LDAP_RECEIVE_TIMEOUT,
            )
            print(f"[LDAP] ✅ Połączono kontem serwisowym: {settings.LDAP_BIND_DN}")

            # Szukamy użytkownika w całym katalogu od ldap_base_dn
            search_filter = f"(&(objectClass=user)(sAMAccountName={username}))"
            service_conn.search(
                search_base=ldap_base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=["distinguishedName", "givenName", "sn", "mail", "memberOf", "mobile"]
            )

            print(f"[LDAP] ✅ Wyniki wyszukiwania: {len(service_conn.entries)}")
            if not service_conn.entries:
                print(f"[LDAP] ❌ Nie znaleziono użytkownika: {username} w {ldap_base_dn}")
                return None

            entry = service_conn.entries[0]
            print(f"[LDAP] ✅ Znalazłem DN: {entry.distinguishedName}")

            # Logowanie właściwego użytkownika
            user_conn = Connection(
                server,
                user=f"{settings.LDAP_DOMAIN}\\{username}",
                password=password,
                auto_bind=True,
                receive_timeout=LDAP_RECEIVE_TIMEOUT,
            )

            if not user_conn.bound:
                print("[LDAP] ❌ Błąd logowania użytkownika (hasło niepoprawne?)")
                return None

            # Pobieramy dane użytkownika
            first_name = str(entry.givenName or "")
            last_name = str(entry.sn or "")
            email = str(entry.mail or "")
            phone_number = str(entry.mobile or "")

            # Tworzymy/aktualizujemy użytkownika w Django
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_unusable_password()

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_active = True
            user.save()

            profile, _ = AdminProfile.objects.get_or_create(user=user)
            profile.first_name = first_name
            profile.last_name = last_name
            profile.email = email
            profile.phone_number = phone_number
            profile.save()

            # Przypisanie grup
            self.assign_groups(user, entry.memberOf)
            print(f"[LDAP] ✅ Grupy przypisane: {[g.name for g in user.groups.all()]}")
            return user

        except Exception as e:
            print(f"[LDAP ERROR] ❌ {e}")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def assign_groups(self, user, ldap_groups):
        mapping = {
            "Recevio_Helpdesk": "Recevio_Helpdesk",
            "Recevio_Reception": "Recevio_Reception",
            "Recevio_User": "Recevio_User",
            "Recevio_BoxFlow": "Recevio_BoxFlow",
            "Recevio_Admin": "Recevio_Admin",
        }

        user.groups.remove(*user.groups.filter(name__startswith="Recevio_"))

        if ldap_groups:
            for group_dn in ldap_groups:
                for ldap_name, django_name in mapping.items():
                    if ldap_name in str(group_dn):
                        django_group, _ = Group.objects.get_or_create(name=django_name)
                        user.groups.add(django_group)

        user.is_staff = user.groups.filter(name="Recevio_Admin").exists()
        user.save()
