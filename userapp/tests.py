from django.test import TestCase
from .models import UserMail
# Create your tests here.

class TestUserMail(TestCase):

    def test_get_email_host(self):
        u_m = UserMail(email_host = 'GM', username = 'nack@gmail.com', password = 'doockie')
        u_m.save()
        self.assertEqual(u_m.get_email_host(), 'smtp.gmail.com')
        

    def test_get_email_port(self):
        u_m = UserMail(email_host = 'GM', username = 'nack@gmail.com', password = 'doockie')
        u_m.save()
        self.assertEqual(u_m.get_email_port(), 587)
