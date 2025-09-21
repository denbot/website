from django.urls.conf import path

from authentication import views

urlpatterns = [
    path("login", views.LoginAPIView.as_view(), name="login"),
    path("login_otp", views.LoginOtpAPIView.as_view(), name="login_otp"),
]