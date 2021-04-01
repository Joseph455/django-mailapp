from django.test import TestCase
from .models import *
# Create your tests here.

class TestMail(TestCase):

    def test_get_recipient_mail_No_value(self):
        ml =  MailList.objects.create(name='Test email list')
        mail = ml.mail_set.create()

        self.assertEqual(mail.get_recipients_mail(), [])

    def test_get_recipient_mail_With_value(self):
        ml =  MailList.objects.create(name='Test email list')
        ml.recipient_set.create(email='testcase@test.com')
        mail = ml.mail_set.create()

        self.assertEqual(mail.get_recipients_mail(), ['testcase@test.com',])
