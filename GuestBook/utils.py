import fitz  # PyMuPDF
from io import BytesIO
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)


def _insert_image_if_exists(page, rect, path):
    """page.insert_image() raises FileNotFoundError for a path whose file is
    gone (e.g. an upload that didn't survive a redeploy — see MEDIA_ROOT in
    settings.py). A missing signature shouldn't crash the whole PDF; skip it
    and leave that spot blank instead."""
    if not path or not os.path.exists(path):
        logger.warning("[BHP PDF] signature file missing, skipping: %s", path)
        return
    page.insert_image(rect, filename=path)


def _resolve_staff_signature_path(visitor):
    """Signature stamped as 'Brüggen employee signature' on the BHP PDF.
    Prefers the host's own fresh signature from the kiosk's 'Confirm guest'
    screen (captured at pickup, specific to this visit); then the saved
    profile signature of whoever approved the registration (the person who
    actually reviewed the safety answers); then the badge-return admin's
    saved profile signature; then a default image."""
    if visitor.host_signature:
        return visitor.host_signature.path
    if visitor.approved_by and hasattr(visitor.approved_by, "adminprofile") and visitor.approved_by.adminprofile.signature:
        return visitor.approved_by.adminprofile.signature.path
    if visitor.returned_by and hasattr(visitor.returned_by, "adminprofile") and visitor.returned_by.adminprofile.signature:
        return visitor.returned_by.adminprofile.signature.path
    return os.path.join(settings.BASE_DIR, "GuestBook", "static", "images", "default_signature.png")


def generate_bhp_pdf(visitor):
    lang = visitor.language if visitor.language in ['pl', 'en'] else 'pl'
    template_path = f'GuestBook/static/pdf/zasady_bhp_{lang}.pdf'
    doc = fitz.open(template_path)
    page = doc[-1]
    font_size = 10
    staff_signature = _resolve_staff_signature_path(visitor)

    if lang == 'pl':
        page.insert_text((100, 750), f"{visitor.start_time.strftime('%d.%m.%Y')}", fontsize=font_size)
        page.insert_text((260, 750), f"{visitor.factory}", fontsize=font_size)
        page.insert_text((430, 750), f"{visitor.first_name} {visitor.last_name}", fontsize=font_size)
        page.insert_text((100, 395), f"{visitor.safety_question_1 or '-'}", fontsize=font_size)
        page.insert_text((290, 420), f"{visitor.safety_question_2 or '-'}", fontsize=font_size)

        # ✅ Podpis graficzny - visitor
        if visitor.signed:
            _insert_image_if_exists(page, fitz.Rect(50, 750, 200, 800), visitor.signed.path)

        # ✅ Podpis graficzny - staff
        _insert_image_if_exists(page, fitz.Rect(320, 755, 470, 805), staff_signature)

    else:  # English
        page.insert_text((100, 720), f"{visitor.start_time.strftime('%d.%m.%Y')}", fontsize=font_size)
        page.insert_text((260, 720), f"{visitor.factory}", fontsize=font_size)
        page.insert_text((420, 720), f"{visitor.first_name} {visitor.last_name}", fontsize=font_size)
        page.insert_text((100, 354), f"{visitor.safety_question_1 or '-'}", fontsize=font_size)
        page.insert_text((290, 372), f"{visitor.safety_question_2 or '-'}", fontsize=font_size)

        if visitor.signed:
            _insert_image_if_exists(page, fitz.Rect(95, 715, 245, 765), visitor.signed.path)

        _insert_image_if_exists(page, fitz.Rect(350, 730, 500, 780), staff_signature)

    pdf_stream = BytesIO()
    doc.save(pdf_stream)
    pdf_stream.seek(0)
    return pdf_stream


from urllib.parse import unquote

def clean_next_url(url, max_depth=10):
    if not url:
        return ''
    for _ in range(max_depth):
        decoded = unquote(url)
        if decoded == url:
            break
        url = decoded
    if 'next=' in url or '/login' in url:
        return ''
    return url
