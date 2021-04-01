from django import forms
from django.contrib.auth.models import User
# create your forms


class LoginForm(forms.Form):
	username = forms.CharField(max_length=200)
	password = forms.CharField(max_length=200)


class RegistrationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			"first_name",
			"last_name",
			"username",
			"password",
			"email"
		]
		widgets = {
			"username": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Enter your username",
			}),
			"password": forms.PasswordInput(attrs={
				"class": "form-control",
				"placeholder": "Enter your password",
			}),
			"first_name": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Enter Your first name",
			}),
			"last_name": forms.TextInput(attrs={
				"class": "form-control",
				"placeholder": "Enter Your last name"
			}),
			"email": forms.EmailInput(attrs={
				"class": "form-control",
				"placeholder": "Enter Your Email addresss ",
			}),
		}


class ForgotPasswordForm(forms.Form):
	username = forms.CharField(max_length=200)
	email = forms.EmailField()


class ActivateAccount(forms.Form):
	username = forms.CharField(max_length=200)
	password = forms.CharField(max_length=200)
