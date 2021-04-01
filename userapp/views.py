from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from . import forms, extras, msgs
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.mail import BadHeaderError
from django.core.exceptions import ObjectDoesNotExist
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from datetime import timedelta
from django.http import HttpResponse
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return redirect(reverse("mailapp:panel"))
    else:
        return render(request, "userapp/home.html")


def account(request):
    context = {
        "loginform": forms.LoginForm(),
        "registrationform": forms.RegistrationForm,
    }
    return render(request, "userapp/account.html", context)


def registration(request):
    if request.POST:
        user_form = forms.RegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            new_user = get_object_or_404(User, username=user_form.cleaned_data['username'])
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False  # Set to inactive so that user has to confirm email before ist login
            new_user.save()
            signer = TimestampSigner(salt="confirm email")
            email_signature = signer.sign(value=new_user.email)
            id_signature = signer.sign(value=str(new_user.id))
            [subject, from_, to_] = ['M-sender Confirm email', 'msenderdesk@gmail.com', new_user.email]
            [html_content,
             text_content] = msgs.confirm_email_message(
                                    id_signature,
                                    email_signature,
                                    '127.0.0.1:8000/account/confirm'
                            )
            try:
                mail = EmailMultiAlternatives(
                    subject,
                    text_content,
                    from_,
                    [to_],
                )
                mail.attach_alternative(html_content, 'text/html')
                mail.send(fail_silently=False)
            except BadHeaderError:
                messages.add_message(request, messages.SUCCESS, "Just one more step left")
                messages.add_message(request, messages.SUCCESS, "Check your email to confirm your account")
                return redirect(reverse("userapp:account"))
            else:
                messages.add_message(request, messages.SUCCESS, "Just one more step left")
                messages.add_message(request, messages.SUCCESS, "Check your email to confirm your account")
                return redirect(reverse("userapp:account"))
        else:
            messages.add_message(request, messages.ERROR, user_form.errors)
            return redirect(reverse("userapp:account"))
    else:
        return redirect(reverse("userapp:account"))


def confirm_email(request, id_signature, email_signature):
    signer = TimestampSigner(salt="confirm email")
    try:
        email = signer.unsign(value=email_signature, max_age=timedelta(minutes=5))
        user_id = signer.unsign(value=id_signature, max_age=timedelta(minutes=5))
    except SignatureExpired:
        return HttpResponse("<h1>This confirmation mail has expired</h1>")
    except BadSignature:
        return HttpResponse("<h1>Bad Signature </h1>")
    else:
        user = get_object_or_404(User, email=email, pk=user_id)
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Your account has been activated!')
        return redirect(reverse("userapp:account"))


def login_view(request):
    if request.POST:
        log = forms.LoginForm(request.POST)
        if log.is_valid():
            user = authenticate(request,
                                username=log.cleaned_data['username'],
                                password=log.cleaned_data['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse("mailapp:panel"))
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "This user is not active. Confirm your email to login"
                    )
                    return redirect(reverse("userapp:index"))
            else:
                messages.add_message(request, messages.ERROR, "invalid username or password!")
                return redirect(reverse("userapp:index"))
        else:
            messages.add_message(request, messages.ERROR, 'Please fill all required fileds of the form')
            return redirect(reverse("userapp:index"))
    return redirect(reverse("userapp:index"))


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "logout successful")
    return redirect(reverse("userapp:account"))


def forgot_password(request):
    if request.POST:
        details = forms.ForgotPasswordForm(request.POST)
        if details.is_valid():
            try:
                user = User.objects.get(
                    username=details.cleaned_data['username'],
                    email=details.cleaned_data['email'])
            except ObjectDoesNotExist:
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'New password has been sent to this email %s' % details.cleaned_data['email']
                )
                return redirect(reverse('userapp:account'))
            else:
                password = extras.password_generator()
                user.set_password(password)
                user.save()
                message = ("Your  request to reset password has been processed. Your new password is %s " % password)
                subject, from_, to_ = 'M-Sender Password Reset', 'msenderdesk@gmail.com', user.email
                try:
                    send_mail(
                        subject,
                        message,
                        from_,
                        [to_],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'New password has been sent to this email %s' % user.email
                    )
                    return redirect(reverse('userapp:account'))
                else:
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        'New password has been sent to this email %s' % user.email
                    )
                    return redirect(reverse('userapp:account'))
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Error please fill all form fields'
            )
            return redirect(reverse('userapp:account'))
    else:
        return redirect(reverse('userapp:account'))


def activate_account(request):
    if request.POST:
        details = forms.ActivateAccount(request.POST)
        if details.is_valid():
            try:
                user = User.objects.get(
                    username=request.POST.get('username'),
                )
            except ObjectDoesNotExist:
                messages.add_message(request, messages.SUCCESS, 'A confirmation mail has been sent to your email')
                return redirect(reverse('userapp:account'))
            else:
                if (user.is_active is False) and (user.check_password(request.POST.get("password"))):
                    signer = TimestampSigner(salt="confirm email")
                    email_signature = signer.sign(user.email)
                    id_signature = signer.sign(user.id)
                    subject, from_email, to_email = 'M-sender Activate account', 'msenderdesk@gmail.com', user.email
                    [html_content,
                     text_content] = msgs.confirm_email_message(
                                                id_signature,
                                                email_signature,
                                                '127.0.0.1:8000/account/confirm'
                                    )
                    try:
                        message = EmailMultiAlternatives(
                                        subject,
                                        html_content,
                                        from_email=from_email,
                                        to=[to_email]
                                )
                        message.attach_alternative(text_content, "text/plain")
                        message.content_subtype = "html"
                        message.send()
                    except BadHeaderError:
                        return HttpResponse('<h2>Invalid Header Found</h2>')
                    else:
                        messages.add_message(request, messages.SUCCESS,
                                             'A confirmation mail has been sent to your email')
                        return redirect(reverse('userapp:account'))
                else:
                    messages.add_message(
                        request,
                        messages.INFO,
                        'Invalid Credentials or your account is already active'
                    )
                    return redirect(reverse('userapp:account'))
        else:
            messages.add_message(request, messages.ERROR, 'invalid credentials!')
            return redirect(reverse('userapp:account'))
    else:
        return redirect(reverse('userapp:account'))
