# mailapp urls

from django.urls import path
from . import views

app_name = 'mailapp'
urlpatterns = [

    # profile section
    path('', views.panel, name='panel'),
    path('instructions/', views.instructions_page, name='instructions'),
    path("profile/", views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='changepassword'),
    path('profile/edit-profile/', views.edit_profile,  name='editprofile'),
    path('profile/deactivate-account/', views.deactivate_account, name='deactivateaccount'),
    path('profile/delete-account/', views.delete_account, name='delete-account'),


    # mail section
    path('mail/', views.mail, name='mail'),
    path("mail/send/", views.sendmail, name="sendmail"),


    # carrier-mail section
    path('carrier-mails/', views.carrier_mail,  name='carriermail'),
    path('carrier-mails/add-mail/', views.add_carrier_mail, name='addcarriermail'),
    # path('carrier-mails/<int:mail_id>-edit-mail/', views.edit_carrier_mail, name='editcarriermail'),
    path('carrier-maiils/<int:mail_id>-delete-mail/', views.delete_carrier_mail, name='deletecarriermail'),


    # mailing list section
    path('mail-lists/', views.mail_list_all, name='maillistall'),
    path('mail-lists/add/', views.add_mail_list, name='addmaillist'),
    path('mail-lists/list-<int:mail_list_id>-edit/', views.edit_mail_list, name='editmaillist'),
    path('mail-lists/list-<int:mail_list_id>-delete/', views.delete_mail_list, name='deletemaillist'),
    path('mail-lists/list-<int:mail_list_id>/', views.mail_list, name='maillist'),
    #                   ---- recipient section -----
    path('mail-lists/list-<int:mail_list_id>-add-recipient/', views.add_recipient, name='addrecipient'),
    path('mail-lists/list-<int:mail_list_id>-import-recipients/', views.import_recipient, name='importrecipients'),
    path('mail-lists/list-<int:mail_list_id>/delete-recipient-<int:recipient_id>/', views.delete_recipient, name='deleterecipient'),
    path('mail-lists/list-<int:mail_list_id>/edit-recipient-<int:recipient_id>/', views.edit_recipient, name='editrecipient'),

    ]
