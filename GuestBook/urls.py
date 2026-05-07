from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_redirect, name='index_redirect'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('start', views.start_registration, name='start'),
    path('language/', views.choose_language, name='choose_language'),
    path('choose_method/', views.choose_method_view, name='choose_method'),
    path('enter_id/', views.enter_visitor_id, name='enter_id'),
    path('guest_form/<str:visitor_id>/', views.guest_form, name='guest_form'),
    path('api/get-host/', views.get_host_for_company, name='get_host_for_company'),
    path('signature/<str:visitor_id>/', views.signature_form, name='signature_form'),
    # path('safety/<str:visitor_id>/', views.safety_form, name='safety_form'),
    path('safety_pdf/<str:visitor_id>/', views.safety_pdf_only, name='safety_pdf_only'),
    path('safety_question1/<str:visitor_id>/', views.safety_question1_view, name='safety_question1'),
    path('safety_question2/<str:visitor_id>/', views.safety_question2_view, name='safety_question2'),
    path('safety_question3/<str:visitor_id>/', views.safety_question3_view, name='safety_question3'),
    path('prepare_visitor/<str:visitor_id>/', views.prepare_visitor, name='prepare_visitor'),
    path('supervision/<str:visitor_id>/', views.supervision_form, name='supervision_form'),
    path('complete/<str:visitor_id>/', views.finish_registration, name='finish_registration'),

    path('enter_badge/', views.enter_badge_view, name='enter_badge'),
    path('guest_form_badge/', views.guest_form_badge, name='guest_form_badge'),
    path('production/<str:visitor_id>/', views.production_form, name='production_form'),
    path('received_badge/<str:visitor_id>/', views.received_badge_view, name='received_badge'),
    path('enter_visitor_id_for_badge/<str:visitor_id>/', views.enter_visitor_id_for_badge, name='enter_visitor_id_for_badge'),
    path('safety_pdf_trusted/<str:visitor_id>/', views.safety_pdf_trusted_view, name='safety_pdf_trusted'),
    path('bhp_question1_trusted/<str:visitor_id>/', views.bhp_question1_trusted_view, name='bhp_question1_trusted'),
    path('bhp_question2_trusted/<str:visitor_id>/', views.bhp_question2_trusted_view, name='bhp_question2_trusted'),
    path('bhp_question3_trusted/<str:visitor_id>/', views.bhp_question3_trusted_view, name='bhp_question3_trusted'),
    path('signature_trusted/<str:visitor_id>/', views.signature_trusted_view, name='signature_trusted'),
    path('complete_trusted/<str:visitor_id>/', views.finish_registration_trusted_view, name='finish_registration_trusted'),

    # path('enter_code/', views.enter_code_view, name='enter_code'),  # Reservations disabled
    # path('enter_visitor_id_for_code/<str:visitor_id>/', views.enter_visitor_id_for_code, name='enter_visitor_id_for_code'),  # Reservations disabled
    # path('signature_code/', views.signature_from_code_view, name='signature_from_code'),  # Reservations disabled
    # path('safety_pdf_code/', views.safety_from_code_view, name='safety_from_code'),  # Reservations disabled
    # path('bhp_question1_code/', views.bhp_question1_from_code_view, name='bhp_question1_from_code'),  # Reservations disabled
    # path('bhp_question2_code/', views.bhp_question2_from_code_view, name='bhp_question2_from_code'),  # Reservations disabled
    # path('bhp_question3_code/', views.bhp_question3_from_code_view, name='bhp_question3_from_code'),  # Reservations disabled
    # path('finalize_code/', views.finalize_from_code_view, name='finalize_from_code'),  # Reservations disabled
    # path("complete_code/<int:reservation_id>/", views.complete_code_view, name="complete_code"),  # Reservations disabled

    path('kiosk/exit/', views.exit_badge_view, name='exit_badge'),
    path("kiosk/exit/done/<str:visitor_id>/", views.exit_done_view, name="exit_done"),
    path('kiosk/settings/', views.kiosk_settings_save, name='kiosk_settings_save'),

    path('panel/', views.dashboard, name='dashboard'),
    path('guest/<int:pk>/', views.visitor_detail, name='visitor_detail'),
    path('generate_bhp_pdf/<int:pk>/', views.generate_bhp_pdf_view, name='generate_bhp_pdf'),
    path('nearby/', views.nearby_persons, name='nearby_persons'),
    path('return/<int:pk>/', views.mark_returned, name='mark_returned'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('approvals/', views.pending_approvals, name='pending_approvals'),
    path('approve/<int:pk>/', views.approve_visitor, name='approve_visitor'),
    # path('coming-visitors/', views.coming_visitors_view, name='coming_visitors'),  # Reservations disabled
    # path('reservations/', views.reservation, name='reservation'),  # Reservations disabled
    # path('reservations/new/', views.reservation_create_view, name='reservation_create'),  # Reservations disabled
    # path('reservation/edit/<int:pk>/', views.reservation_edit_view, name='reservation_edit'),  # Reservations disabled
    # path('reservations/cancel/<int:pk>/', views.reservation_cancel_view, name='reservation_cancel'),  # Reservations disabled
    # path('reservations/<int:pk>/resend-sms/', views.reservation_resend_sms_view, name='reservation_resend_sms'),  # Reservations disabled
    path('profile/', views.profile_view, name='profile'),
    path('export_excel/', views.export_visitors_excel, name='export_visitors_excel'),
    path('reprint/<int:pk>/', views.reprint_badge_view, name='reprint_badge'),


    path("companies/", views.companies_view, name="companies"),
    path("companies/add/", views.company_add, name="company_add"),
    path("companies/<int:pk>/edit/", views.company_edit, name="company_edit"),
    path("companies/<int:pk>/delete/", views.company_delete, name="company_delete"),
    path("companies/import/", views.company_import, name="company_import"),

    path("hosts/", views.hosts_view, name="hosts"),
    path("hosts/add/", views.host_add, name="host_add"),
    path("hosts/<int:pk>/edit/", views.host_edit, name="host_edit"),
    path("hosts/<int:pk>/delete/", views.host_delete, name="host_delete"),
    path("hosts/import/", views.host_import, name="host_import"),

    path("trusted/", views.trusted_view, name="trusted"),
    path("trusted/add/", views.trusted_add, name="trusted_add"),
    path("trusted/<int:pk>/edit/", views.trusted_edit, name="trusted_edit"),
    path("trusted/<int:pk>/delete/", views.trusted_delete, name="trusted_delete"),

    path("visitor/<int:pk>/edit/", views.visitor_edit_view, name="visitor_edit"),
    # path("reservations_visitors/", views.reservation_visitor_view, name="reservation_visitor"),  # Reservations disabled
    # path("reservations_visitors/<int:pk>/edit/", views.reservation_visitor_edit_view, name="reservation_visitor_edit"),  # Reservations disabled
    # path("reservations/add/", views.reservation_add_view, name="reservation_add"),  # Reservations disabled

    path('helpdesk/users/', views.helpdesk_user_list, name='helpdesk_users'),
    path('helpdesk/users/<int:uid>/', views.helpdesk_user_edit, name='helpdesk_user_edit'),

    path("boxflow/add/", views.boxflow_scan_label, name="boxflow_add"),
    path("boxflow/add/confirm/", views.boxflow_add_pack, name="boxflow_add_confirm"),
    path("boxflow/list/", views.boxflow_pack_list, name="boxflow_list"),
    path('boxflow/<int:pk>/delete/', views.boxflow_delete_pack, name='boxflow_delete'),
    path("boxflow/inbox/", views.boxflow_inbox_status, name="boxflow_inbox"),
    path("boxflow/out/", views.boxflow_pack_out, name="boxflow_out"),
    path("boxflow/<int:pk>/", views.boxflow_pack_detail, name="boxflow_detail"),
    path("boxflow/<int:pk>/reprint/", views.boxflow_reprint_label, name="boxflow_reprint"),

    # helpdesk / support center
    path("support/senders/", views.helpdesk_senders, name="helpdesk_senders"),
    path("support/recipients/", views.helpdesk_recipients, name="helpdesk_recipients"),
    path("support/import/senders/", views.helpdesk_import_senders, name="helpdesk_import_senders"),
    path("support/import/recipients/", views.helpdesk_import_recipients, name="helpdesk_import_recipients"),
    path("support/package/<int:pk>/edit/", views.helpdesk_package_edit, name="helpdesk_package_edit"),

    path("admin/test-email/", views.test_email_view, name="test_email"),

    path("kiosk/pickup/", views.public_pickup_view, name="public_pickup"),

    path("boxflow/<int:pk>/zpl/", views.boxflow_get_zpl, name="boxflow_get_zpl"),
    path("visitor/<int:pk>/zpl/", views.visitor_get_zpl, name="visitor_get_zpl"),

]
