from django import forms
from . import models


class AddCarrierMail(forms.Form):
    username = forms.EmailField(max_length=200)
    host = forms.CharField(max_length=2)


class AddMailList(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=150)


class EditMailListForm(forms.Form):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=300)


class EditProfileForm(forms.Form):
    username = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    first_name = forms.CharField(max_length=200)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length=200)
    confirm_password = forms.CharField(max_length=200)


class AddRecipient(forms.Form):
    email = forms.EmailField()

class ImportRecipients(forms.Form):
    import_from = forms.CharField(max_length=50)


class SendMail(forms.Form):
    message = forms.CharField(max_length=200)
    subject = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    mailcarrier = forms.IntegerField()
    mailinglist = forms.IntegerField()
