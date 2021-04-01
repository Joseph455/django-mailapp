# pylint:disable=E0001
# pylint:disable=E0001
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


# Create your models here.

# change blank to false for related fileds later


class CarrierMail(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    username = models.EmailField(blank=False)
    mail_choices = (
        ('GM', 'Google mail'),
        ('YM', 'Yahoo mail'),
    )
    email_host = models.CharField(max_length=2, choices=mail_choices, null=False, default='GM')
    confirmed = models.BooleanField(default=True)  # set default to false later

    def is_confirmed(self):
        if self.confirmed:
            return True
        else:
            return False

    def __str__(self):
        return str(self.username)

    def get_email_host(self):
        hosts = {
            'GM': 'smtp.gmail.com',
            'YM': 'smtp.mail.yahoo.com',
        }
        if self.email_host in hosts:
            # noinspection PyTypeChecker
            return hosts[self.email_host]

    def get_email_port(self):
        hosts = {
            'GM': 587,
            'YM': 465,
        }
        if self.email_host in hosts:
            # noinspection PyTypeChecker
            return hosts[self.email_host]


class MailList(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True)


    def __str__(self):
        return self.name


class Recipient(models.Model):
    email = models.EmailField(blank=False)
    owners = models.ForeignKey(MailList, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    def get_position(self):
        recipient_lst = list(self.owners.recipient_set.all().order_by('-date_created'))
        return str(recipient_lst.index(self) + 1)


class Mail(models.Model):
    send_to = models.ForeignKey(MailList, null=True, on_delete=models.SET_NULL, blank=True)
    send_by = models.ForeignKey(CarrierMail, null=True, on_delete=models.SET_NULL, blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField(blank=True)

    def get_recipients_mail(self):
        return [recp.email for recp in self.send_to.recipient_set.all()]


class Action(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True)
    name = models.CharField(max_length=200, blank=False)
    actions = [
        ('DL', 'Deleted'),
        ('CR', 'Created'),
        ('CD', 'Changed'),
        ('ED', 'Edited'),
        ('ST', 'Sent'),
        ('AD', 'Added'),
        ('IM', 'Imported')
    ]
    action = models.CharField(max_length=2, choices=actions, default='ED')
    time = models.DateTimeField(default=timezone.now)

    # You track the actions using views.py

    def is_recent(self):
        if timezone.now() <= (self.time + datetime.timedelta(hours=24)):
            return True
        else:
            return False


class RecentMail(models.Model):
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    subject = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    successful = models.IntegerField()
    unsuccessful = models.IntegerField()
    mailing_list = models.EmailField()

    def is_recent(self):
        if timezone.now() <= (self.date + datetime.timedelta(days=1)):
            return True
        else:
            return False


class Instructions(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = 'instruction'




