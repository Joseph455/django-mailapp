from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from .models import *
from . import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.mail import get_connection, EmailMessage, BadHeaderError


# Create your views here.


@login_required
def panel(request):
    num_of_recipients = 0
    for maillist in request.user.maillist_set.all():
        num_of_recipients += len(maillist.recipient_set.all())
    context = {
        'actions': request.user.action_set.all().order_by("-time")[:9],
        'num_maillist': len(request.user.maillist_set.all()),
        'num_recipient': num_of_recipients,
    }
    return render(request, 'mailapp/panel.html', context)


@login_required
def instructions_page(request):
    context = {
        'instructions': Instructions.objects.all(),
    }
    return render(request, 'mailapp/instructions.html', context)


# --------------------- USER MAIL SECTION-----------------------------#
@login_required
def carrier_mail(request):
    context = {
        "carrier_mails": request.user.carriermail_set.all(),
        "carriermailform": forms.AddCarrierMail,
    }
    return render(request, 'mailapp/carriermail.html', context)


@login_required
def add_carrier_mail(request):
    if request.POST:
        add_mail = forms.AddCarrierMail(request.POST)
        if add_mail.is_valid():
            if len(request.user.carriermail_set.all()) < 3:
                carrier = request.user.carriermail_set.get_or_create(username=add_mail.cleaned_data['username'],
                                                                     email_host=add_mail.cleaned_data['host'])
                if carrier[1] is False:
                    messages.add_message(request, messages.SUCCESS, "This mail already exits")
                    return redirect(reverse("mailapp:carriermail"))
                else:
                    request.user.action_set.create(
                        name='Mail Carrier',
                        action='CR'
                    )
                    messages.add_message(request, messages.SUCCESS, "Carrier Mail added successfully!")
                    return redirect(reverse('mailapp:carriermail'))
            else:
                messages.add_message(request, messages.ERROR, "Error You reached the carrier mail limit of 3")
                return redirect(reverse("mailapp:carriermail"))
        else:
            messages.add_message(request, messages.SUCCESS, "Please add a valid email address")
            return redirect(reverse('mailapp:carriermail'))
    else:
        return redirect(reverse('mailapp:carriermail'))


@login_required
def delete_carrier_mail(request, mail_id):
    mail_ = get_object_or_404(CarrierMail, pk=mail_id)
    mail_.delete()
    messages.add_message(request, messages.SUCCESS, 'Carrier Mail has been successfully deleted')
    request.user.action_set.create(
        name='Mail Carrier',
        action='DL'
    )
    return redirect(reverse('mailapp:carriermail'))


# @login_required
# def edit_carrier_mail(request, mail_id):
#     if request.POST:
#         mail_list = get_object_or_404(CarrierMail, pk=mail_id)
#         change = forms.AddUserMail(request.POST)
#         if change.is_valid():
#             mail_list.username = change.username
#             mail_list.email_host = change.email_host
#             mail_list.save()
#             action = request.user.action_set.create(name='Mail', action='ED')
#             action.save()
#             request.user.action_set.create(
#                 name='Mail Carrier',
#                 action='ED'
#             )
#             return redirect(reverse('mailapp:carriermail'))
#         else:
#             return redirect(reverse('mailapp:carriermail'))
#     else:
#         return redirect(reverse('mailapp:carriermail'))


# ---------------------MAIL LIST SECTION-----------------------------#
@login_required
def mail_list_all(request):
    mailing_list = request.user.maillist_set.all()
    context = {
        'mailinglists': mailing_list,
        'maillistform': forms.AddMailList,
    }
    return render(request, 'mailapp/maillists.html', context)


@login_required
def add_mail_list(request):
    if request.POST:
        new_mail_list = forms.AddMailList(request.POST)
        if new_mail_list.is_valid():
            if len(request.user.maillist_set.all()) < 3:
                new_mail = request.user.maillist_set.get_or_create(
                                        name=new_mail_list.cleaned_data['name'],
                                        description=new_mail_list.cleaned_data['description'])
                if new_mail[1] is False:
                    messages.add_message(request, messages.SUCCESS, "Mail List with this name already exist")
                    request.user.action_set.create(
                        name='Mailing List',
                        action='CR'
                    )
                    return redirect(reverse("mailapp:maillistall"))
                else:
                    messages.add_message(request, messages.SUCCESS, 'Successfully created mailing list')
                    return redirect(reverse("mailapp:maillistall"))
            else:
                messages.add_message(request, messages.ERROR, 'Error You have reached the mailing list limit of 3')
                return redirect(reverse("mailapp:maillistall"))
        else:
            messages.add_message(request, messages.ERROR, 'Error! Please fill the form Field')
            return redirect(reverse("mailapp:maillistall"))
    else:
        return redirect(reverse("mailapp:maillistall"))


@login_required
def delete_mail_list(request, mail_list_id):
    mail_ = get_object_or_404(MailList, pk=mail_list_id)
    mail_.delete()
    request.user.action_set.create(
        name='Mailing List',
        action='DL'
    )
    return redirect(reverse("mailapp:maillistall"))


# -------------------------------RECIPIENT SECTION --------------------------------

@login_required
def mail_list(request, mail_list_id):
    search_result = None
    maillist = get_object_or_404(MailList, pk=mail_list_id)
    recipients = maillist.recipient_set.all().order_by('-date_created')
    if request.GET:
        search_value = request.GET.get('search')
        if search_value:
            search_result = maillist.recipient_set.all().filter(email__icontains=search_value)[:10]
            if not search_result:
                messages.add_message(request, messages.ERROR, 'No recipient matches query!')
        else:
            messages.add_message(request, messages.ERROR, 'No recipient matches query!')

    print(str(messages.get_level(request)).upper())
    context = {
        'recipients': recipients,
        'addrecipientform': forms.AddRecipient,
        'maillist': maillist,
        "maillists": request.user.maillist_set.all(),
        'search_result': search_result,
    }
    return render(request, 'mailapp/maillist.html', context)


@login_required
def edit_mail_list(request, mail_list_id):
    if request.POST:
        mail_list__ = get_object_or_404(MailList, pk=mail_list_id)
        changes = forms.EditMailListForm(request.POST)
        if changes.is_valid():
            mail_list__.name = changes.cleaned_data['name']
            mail_list__.description = changes.cleaned_data['description']
            mail_list__.save()
            messages.add_message(request, messages.SUCCESS, "Changes made successfully!")
            request.user.action_set.create(
                name='Mailing List',
                action='ED'
            )
            return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))
        else:
            messages.add_message(request, messages.ERROR, 'could not make changes! ')
            return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))
    return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))


@login_required
def import_recipient(request, mail_list_id):
    if request.POST:
        form = forms.ImportRecipients(request.POST)
        if form.is_valid():
            import_to = get_object_or_404(MailList, pk=mail_list_id)
            import_from = get_object_or_404(MailList, pk=form.cleaned_data["import_from"])
            recipients_email = [recipient.email for recipient in import_from.recipient_set.all()]
            num = len(recipients_email)
            for mail__ in recipients_email:
                import_to.recipient_set.get_or_create(email=mail__)
            messages.add_message(request, messages.SUCCESS, ("%s" % num + " recipients imported"))
            request.user.action_set.create(
                name=str(num) + 'Recipient(s)',
                action='IM'
            )
            return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))
        else:
            messages.add_message(request, messages.ERROR, "Import failed.")
            return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))
    return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))


@login_required
def add_recipient(request, mail_list_id):
    if request.POST:
        maillist = get_object_or_404(MailList, pk=mail_list_id)
        new_recipient = forms.AddRecipient(request.POST)
        if new_recipient.is_valid():
            new_recipient = maillist.recipient_set.get_or_create(email=new_recipient.cleaned_data['email'])
            if new_recipient[1] is False:
                messages.add_message(request, messages.SUCCESS, "Recipient with this email already exist")
                request.user.action_set.create(
                    name='Recipient',
                    action='AD'
                )
                return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))
            else:
                return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))
        else:
            messages.add_message(request, messages.SUCCESS, "Invalid Email")
            return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))
    return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))


@login_required
def edit_recipient(request, mail_list_id, recipient_id):
    if request.POST:
        recipient = get_object_or_404(MailList, pk=mail_list_id).recipient_set.get(pk=recipient_id)
        changes = forms.AddRecipient(request.POST)
        if changes.is_valid():
            recipient.email = request.POST.get('email')
            recipient.save()
            request.user.action_set.create(
                name='Recipient',
                action='ED'
            )
            return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))
        else:
            return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))
    else:
        return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))


@login_required
def delete_recipient(request, mail_list_id, recipient_id):
    recipient = get_object_or_404(Recipient, pk=recipient_id)
    recipient.delete()
    request.user.action_set.create(
        name='Recipient',
        action='DL'
    )
    return redirect(reverse("mailapp:maillist", args=(mail_list_id,)))


# ------------------------Mail Section--------------------------------------


@login_required
def mail(request):
    context = {
        "mailcarriers": request.user.carriermail_set.all(),
        "mailinglists": request.user.maillist_set.all(),
        "recentmails": request.user.recentmail_set.all().order_by('-date')[:7],
    }
    return render(request, "mailapp/mail.html", context)


@login_required
def sendmail(request):
    if request.POST:
        form = forms.SendMail(request.POST)
        if form.is_valid():
            # prepare data required to send email
            by = get_object_or_404(CarrierMail, pk=form.cleaned_data["mailcarrier"])
            to = get_object_or_404(MailList, pk=form.cleaned_data["mailinglist"])
            subj = form.cleaned_data['subject']
            msg = form.cleaned_data['message']
            password = form.cleaned_data['password']
            connection = get_connection(
                host=by.get_email_host(),
                port=by.get_email_port(),
                username=by.username,
                password=password,
                use_tls=True,
                fail_silently=False,
            )
            connection.open()
            successful = 0

            for recipient in to.recipient_set.all():
                try:
                    successful += EmailMessage(subj, msg, by, [recipient.email], connection=connection).send()
                except BadHeaderError:
                    continue
            connection.close()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Meesages sent. Successful %s" % successful + "unsuccessful %s" % (len(
                    to.recipient_set.all()) - successful),
            )

            # add the message to recently sent mail
            request.user.recentmail_set.create(
                successful=successful,
                unsuccessful=len(to.recipient_set.all()) - successful,
                subject=subj,
                mailing_list=to,
            )
            request.user.action_set.create(
                name='Mail %s' % subj,
                action='ST'
            )
            return redirect(reverse("mailapp:mail"))
        else:
            messages.add_message(request, messages.ERROR, "make sure all fields are filled")
            return redirect(reverse("mailapp:mail"))
    else:
        return redirect(reverse("mailapp:mail"))


# ---------------------------------PROFILE SECTION ------------------------------------

@login_required
def profile(request):
    return render(request, 'mailapp/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.POST:
        change = forms.EditProfileForm(request.POST)
        if change.is_valid():
            request.user.username = change.cleaned_data['username']
            # request.user.email = change.cleaned_data['email']
            request.user.last_name = change.cleaned_data['last_name']
            request.user.first_name = change.cleaned_data['first_name']
            request.user.save()
            messages.add_message(request, messages.SUCCESS, 'Change successful!')
            request.user.action_set.create(
                name='Profile',
                action='ED'
            )
            return redirect(reverse('mailapp:profile'))
        else:
            messages.add_message(request, messages.ERROR, 'Please fill all required fileds of the form')
            return redirect(reverse('mailapp:profile'))
    else:
        return redirect(reverse('mailapp:profile'))


@login_required
def change_password(request):
    if request.POST:
        new_password = forms.ChangePasswordForm(request.POST)
        if new_password.is_valid():
            if new_password.cleaned_data['password'] == new_password.cleaned_data['confirm_password']:
                request.user.set_password(new_password.cleaned_data['password'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.add_message(request, messages.SUCCESS, 'Password change successful!')
                request.user.action_set.create(
                    name='Password',
                    action='CD'
                )
                return redirect(reverse('mailapp:profile'))
            else:
                messages.add_message(request, messages.ERROR, 'Passwords do not match!')
                return redirect(reverse('mailapp:profile'))
        else:
            messages.add_message(request, messages.ERROR, 'Please fill all required fileds of the form')
            return redirect(reverse('mailapp:profile'))
    else:
        return redirect(reverse('mailapp:profile'))


@login_required
def deactivate_account(request):
    request.user.is_active = False
    request.user.save()
    messages.add_message(request, messages.SUCCESS, "Account deactivated successfully")
    return redirect(reverse("userapp:logout"))


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    messages.add_message(request, messages.SUCCESS, "Your account has been deleted successfully")
    return redirect(reverse("userapp:logout"))
