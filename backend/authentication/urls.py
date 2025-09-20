from django.urls.conf import path

from authentication import views

urlpatterns = [
    path("login", views.LoginFormView.as_view(), name="login"),
    path("login_otp", views.LoginOtpFormView.as_view(), name="login_otp"),
]