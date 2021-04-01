from django.urls import path
from . import views

app_name = "userapp"

urlpatterns = [
	path("", views.home, name="index"),
	path("account/", views.account, name="account"),
	path("account/registration/", views.registration, name="registration"),
	path("account/login/", views.login_view, name="login"),
	path("account/logout/", views.logout_view, name="logout"),
	path('account/confirm/<id_signature>/<email_signature>/', views.confirm_email, name='confirmemail'),
	path('account/activate/', views.activate_account, name='activateaccount'),
	path('account/reset-password/', views.forgot_password, name='forgotpassword'),
]
